import os, sys, socket, time, logging, threading, pickle, random, subprocess, gc, numpy as np
from collections import deque
import cv2, face_recognition
from flask import Flask, render_template, Response, jsonify, request
from PIL import Image
import requests
import queue

# --- CONFIGURATION ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("Nikki")
app = Flask(__name__)
SERVER_START = time.time()

# --- PROCESS CLEANUP ---
def cleanup_background():
    try:
        current_pid = os.getpid()
        # 1. Kill any process on Port 5000
        try:
            # We use subprocess.run for better control and timeout
            cmd_port = ["lsof", "-t", "-i:5000"]
            result = subprocess.run(cmd_port, capture_output=True, text=True)
            pids_port = result.stdout.split()
            for pid in pids_port:
                if int(pid) != current_pid:
                    subprocess.call(['kill', '-9', pid])
                    logger.info(f"Killed process {pid} on port 5000")
        except Exception as e:
            logger.debug(f"Port cleanup skipped: {e}")

        # 2. Kill other python processes running app.py
        try:
            cmd_py = "ps aux | grep 'app.py' | grep -v grep | awk '{print $2}'"
            pids_py = subprocess.check_output(cmd_py, shell=True).decode().split()
            for pid in pids_py:
                if int(pid) != current_pid:
                    subprocess.call(['kill', '-9', pid])
        except: pass
        
        # 3. Release Camera Locks
        camera_procs = ['libcamera', 'camera-stream', 'vlc', 'ffmpeg', 'motion']
        for proc in camera_procs:
            subprocess.call(['pkill', '-9', proc], stderr=subprocess.DEVNULL)
        
        time.sleep(2)
        logger.info("Background cleanup complete.")
    except Exception as e:
        logger.warning(f"Cleanup error: {e}")

cleanup_background()

# --- LOAD ENV ---
def load_env():
    env_path = os.path.join(os.getcwd(), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k.strip()] = v.strip()
        logger.info("Environment variables loaded.")

# --- CONFIG ---
load_env()
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
GROQ_MODEL = "llama-3.1-8b-instant"
VOICE_NAME = "en-US-JennyNeural"
MPG123_PATH = "/usr/bin/mpg123" # Absolute path for reliability

# --- THREAD SAFE STATE ---

# --- THREAD SAFE STATE ---
data_lock = threading.Lock()
face_lock = threading.Lock()
attendance_log = {}
known_encodings, known_names = [], []

# Scene Data
scene_data = {"names": [], "count": 0, "x_pos": 0.5} 
attendance_enabled = True
enroll_mode = False
enroll_name = ""
greeted_log = {} # name -> last_greet_time
GREETING_TIMEOUT = 3600 # 1 hour cooldown for greetings
GREETINGS = [
    "Hello {name}, welcome back.",
    "I see you, {name}.",
    "System online. Greetings, {name}.",
    "Access authorized. Hello {name}.",
    "Welcome, {name}. How can I assist you today?",
    "Subject recognized: {name}. Good to see you."
]

# --- HARDWARE (Mock Fallbacks) ---
sensor_cache = {"cpu": "40°C", "ram": "30%", "net": "WiFi", "aqi": 45, "temp": 26.0, "hum": 60.0, "bat": 100.0}
dht_sensor, mq135 = None, None

try:
    import board, busio, adafruit_dht
    from adafruit_ads1x15.ads1115 import ADS1115
    from adafruit_ads1x15.analog_in import AnalogIn
    
    # Robust P0 handling
    try:
        from adafruit_ads1x15.ads1x15 import P0
    except ImportError:
        P0 = 0  # Fallback if P0 isn't found in module path
    
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS1115(i2c)
    mq135 = AnalogIn(ads, P0)
    dht_sensor = adafruit_dht.DHT22(board.D4, use_pulseio=False)
    logger.info("Hardware Initialized.")
except Exception as e:
    logger.warning(f"Hardware Init Failed (Mock Mode): {e}")

# --- FACE MEMORY ---
FACES_FILE = "trained_faces.pkl"
if os.path.exists(FACES_FILE):
    try:
        with open(FACES_FILE, "rb") as f:
            data = pickle.load(f)
            known_encodings, known_names = data["encodings"], data["names"]
            attendance_log = {n: "Absent" for n in known_names}
            logger.info(f"Loaded {len(known_encodings)} authorized faces from {FACES_FILE}")
    except Exception as e:
        logger.error(f"Failed to load faces file: {e}")
else:
    logger.warning(f"No face memory file found ({FACES_FILE}). Tracking will be 'Unknown' only.")

# --- ROBUST CAMERA INITIALIZATION ---
picam2 = None
usb_cam = None
camera_type = "None"

# 1. Try Pi Camera (CSI) First
try:
    from picamera2 import Picamera2
    logger.info("Attempting Pi Camera (CSI) initialization...")
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"}))
    picam2.start()
    camera_type = "CSI"
    logger.info("SUCCESS: Pi Camera (CSI) initialized.")
except Exception as e:
    logger.warning(f"Pi Camera failed: {e}")
    picam2 = None

# 2. Fallback to USB Camera if Pi Camera failed
if not picam2:
    for attempt in range(3):
        try:
            logger.info(f"Attempting USB Camera fallback (Attempt {attempt+1})...")
            # Using V4L2 backend often helps on Linux/Raspberry Pi
            usb_cam = cv2.VideoCapture(0, cv2.CAP_V4L2)
            if usb_cam.isOpened():
                usb_cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                usb_cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                usb_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                camera_type = "USB"
                logger.info("SUCCESS: USB Camera initialized.")
                break
            else:
                usb_cam = None
                time.sleep(1)
        except Exception as e:
            logger.warning(f"USB Camera Attempt {attempt+1} failed: {e}")
            time.sleep(1)

if not picam2 and not usb_cam:
    logger.error("CRITICAL: No camera available. Running in Mock Mode.")

# --- BACKGROUND LOOPS ---
def sensor_loop():
    while True:
        try:
            t, h = None, None
            if dht_sensor:
                try: t, h = dht_sensor.temperature, dht_sensor.humidity
                except: pass
            
            sys_t, sys_r, sys_n = "N/A", "N/A", "Hotspot"
            try:
                with open("/sys/class/thermal/thermal_zone0/temp") as f: sys_t = f"{int(f.read())/1000:.0f}°C"
                with open('/proc/meminfo') as f:
                    l = f.readlines(); tot, free = int(l[0].split()[1]), int(l[2].split()[1])
                    sys_r = f"{int((tot-free)/tot*100)}%"
                ssid = subprocess.check_output(['iwgetid', '-r'], stderr=subprocess.DEVNULL).decode().strip()
                if ssid: sys_n = ssid
            except: pass

            def get_local_ip():
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                try:
                    s.connect(('10.255.255.255', 1))
                    ip = s.getsockname()[0]
                except:
                    ip = '127.0.0.1'
                finally:
                    s.close()
                return ip

            with data_lock:
                if t: sensor_cache["temp"] = t
                if h: sensor_cache["hum"] = h
                if mq135: sensor_cache["aqi"] = abs(mq135.value / 32767.0 * 100)
                sensor_cache.update({"cpu": sys_t, "ram": sys_r, "net": sys_n, "ip": get_local_ip()})
                sensor_cache["bat"] = max(0, 100.0 - ((time.time()-SERVER_START)/60*0.05))
        except: pass
        time.sleep(2)

threading.Thread(target=sensor_loop, daemon=True).start()

# --- VISION ENGINE ---
# --- VISION ENGINE (Threaded) ---
latest_frame = None
vision_lock = threading.Lock() # Lock for the raw frame buffer
last_locations, last_names = [], []
frame_counter = 0

def vision_worker():
    global last_locations, last_names, latest_frame, scene_data, enroll_mode, enroll_name, attendance_enabled
    
    logger.info("Vision Worker Thread Started.")
    while True:
        try:
            with vision_lock:
                if latest_frame is None:
                    time.sleep(0.01)
                    continue
                # Copy the latest frame for processing to release the lock quickly
                frame = latest_frame.copy()
            
            # 1. Processing (RGB)
            rgb_small = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (0,0), fx=0.5, fy=0.5)
            
            with face_lock:
                locs = face_recognition.face_locations(rgb_small, model="hog")
                
                # Auto-exposure fallback if no faces
                if not locs:
                    img_yuv = cv2.cvtColor(rgb_small, cv2.COLOR_RGB2YUV)
                    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
                    rgb_small = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
                    locs = face_recognition.face_locations(rgb_small, model="hog")
                
                encs = face_recognition.face_encodings(rgb_small, locs)
            
            names = []
            x_vals = []
            
            for (t, r, b, l), enc in zip(locs, encs):
                if enroll_mode and enroll_name:
                    name = enroll_name.lower()
                    # SAVE PHOTO TO DISK
                    img_path = os.path.join("known_faces", f"{name}.jpg")
                    try:
                        cv2.imwrite(img_path, frame)
                        logger.info(f"Photo Saved: {img_path}")
                    except Exception as e:
                        logger.error(f"Failed to save photo: {e}")

                    with data_lock:
                        if name not in known_names:
                            known_names.append(name)
                            known_encodings.append(enc)
                            attendance_log[name] = "Present"
                            with open(FACES_FILE, "wb") as f:
                                pickle.dump({"encodings": known_encodings, "names": known_names}, f)
                            logger.info(f"Auto-Registered: {name}")
                            enroll_mode = False
                            enroll_name = ""
                            attendance_enabled = True
                    names.append(name)
                    continue

                name = "Unknown"
                if known_encodings and attendance_enabled:
                    with face_lock:
                        matches = face_recognition.compare_faces(known_encodings, enc, 0.6)
                    if any(matches):
                        dist = face_recognition.face_distance(known_encodings, enc)
                        name = known_names[np.argmin(dist)]
                        with data_lock: attendance_log[name] = "Present"
                        logger.info(f"Vision Thread Found: {name}")
                
                names.append(name)
                x_vals.append((l + r) / 2 / 320)
                
                # --- PROACTIVE GREETING LOGIC ---
                if name != "Unknown":
                    now = time.time()
                    if name not in greeted_log or (now - greeted_log[name]) > GREETING_TIMEOUT:
                        greeted_log[name] = now
                        msg = random.choice(GREETINGS).format(name=name)
                        logger.info(f"Proactive Greeting for {name}")
                        run_speak(msg)

            # Update shared state
            last_locations = [(t*2, r*2, b*2, l*2) for t,r,b,l in locs]
            last_names = names
            
            with data_lock:
                scene_data["names"] = names
                scene_data["count"] = len(names)
                scene_data["x_pos"] = np.mean(x_vals) if x_vals else 0.5
            
            time.sleep(0.1) # Throttle worker to save CPU
        except Exception as e:
            logger.error(f"Vision Worker Error: {e}")
            time.sleep(1)

threading.Thread(target=vision_worker, daemon=True).start()

def gen_frames():
    global last_locations, last_names, latest_frame
    
    if not picam2 and not usb_cam:
        while True:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Camera Unavailable", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            ret, buf = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')
            time.sleep(1)

    while True:
        try:
            bgr_frame = None
            if picam2:
                rgb = picam2.capture_array()
                bgr_frame = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
            elif usb_cam:
                ret, bgr_frame = usb_cam.read()
            
            if bgr_frame is None:
                time.sleep(0.01)
                continue
            
            # Push to vision worker
            with vision_lock:
                latest_frame = bgr_frame

            # --- RENDER OVERLAYS (Fluid) ---
            # We use the LATEST available results from the worker
            for (t,r,b,l), name in zip(last_locations, last_names):
                color = (0, 255, 0) if name != "Unknown" else (255, 255, 255)
                cv2.rectangle(bgr_frame, (l,t), (r,b), color, 2)
                cv2.rectangle(bgr_frame, (l,b-30), (r,b), color, -1)
                cv2.putText(bgr_frame, name, (l+6, b-6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 2)

            ret, buf = cv2.imencode('.jpg', bgr_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')
            
        except Exception as e:
            logger.error(f"Streaming Error: {e}")
            time.sleep(0.1)

# --- ROUTES ---
@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/video_feed')
def video_feed(): 
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/sensors')
def api_sensors():
    with data_lock:
        d = sensor_cache.copy()
        d["temp_str"] = f"{d['temp']:.1f}°C"
        d["hum_str"] = f"{d['hum']:.1f}%"
        return jsonify(d)

@app.route('/api/status')
def api_status():
    with data_lock: return jsonify(attendance_log)

@app.route('/api/context')
def api_context():
    with data_lock: return jsonify(scene_data)

# --- BULLETPROOF LIVE TTS (Edge-TTS + Absolute Path Player) ---
speak_queue = queue.Queue()

def tts_worker():
    while True:
        text = speak_queue.get()
        if text is None: break
        try:
            logger.info(f"AURA Speaking: {text}")
            
            # Secure execution: no shell=True, avoids command injection vulnerabilities.
            edge_cmd = [sys.executable, "-m", "edge_tts", "--voice", VOICE_NAME, "--text", text, "--write-media", "-"]
            player_cmd = [MPG123_PATH, "-q", "-"]
            
            p1 = subprocess.Popen(edge_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # p2 reads from p1.stdout
            p2 = subprocess.Popen(player_cmd, stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p1.stdout.close() # allow p1 to receive a SIGPIPE if p2 exits.
            
            # Add timeout to prevent worker from hanging indefinitely
            stdout, stderr = p2.communicate(timeout=30)
            
            if p2.returncode != 0:
                logger.error(f"Player/TTS Error: {stderr.decode('utf-8', errors='ignore')}")
                
        except subprocess.TimeoutExpired:
            p1.kill()
            p2.kill()
            p1.communicate()
            p2.communicate()
            logger.error("Vocal Engine Error: Execution timed out. Edge-TTS or player hung.")
        except Exception as e:
            logger.error(f"Vocal Engine Error: {e}")
        speak_queue.task_done()

threading.Thread(target=tts_worker, daemon=True).start()

def run_speak(text):
    if not text: return
    speak_queue.put(text)

@app.route('/api/speak', methods=['POST'])
def api_speak():
    data = request.get_json()
    text = data.get('text', '')
    if text:
        run_speak(text)
        return jsonify({"status": "speaking"})
    return jsonify({"status": "error", "msg": "No text"}), 400

@app.route('/api/ai_process', methods=['POST'])
def ai_process():
    if not GROQ_API_KEY:
        return jsonify({"status": "error", "msg": "API Key missing"}), 401
    
    data = request.get_json()
    text = data.get('text', '')
    
    with data_lock:
        names = scene_data.get("names", [])
        
    system_prompt = f"You are Nikki. Be extremely brief. Situation: People: {', '.join(names) if names else 'None'}."

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                "temperature": 0.5,
                "max_tokens": 50
            },
            timeout=5
        )
        res_data = response.json()
        if "choices" in res_data:
            reply = res_data["choices"][0]["message"]["content"]
            return jsonify({"status": "success", "reply": reply})
        return jsonify({"status": "error", "msg": "Invalid response from AI"}), 500
    except Exception as e:
        logger.error(f"AI Error: {e}")
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route('/api/mark_present', methods=['POST'])
def mark_present():
    data = request.get_json() or {}
    name = data.get('name', '').lower()
    if not name:
        return jsonify({"status": "error", "msg": "No name provided"}), 400
    
    with data_lock:
        # If the person is already known (in known_names), or we just want to track them
        # We'll allow any name to be marked present for now to support TM's dynamic labels
        attendance_log[name] = "Present"
        # If not in known list, let's add them so they show up in Roster headers even if no encoding exists
        if name not in known_names:
             known_names.append(name)
             
    logger.info(f"TM Fallback: {name} marked present.")
    return jsonify({"status": "success"})

@app.route('/api/add_student', methods=['POST'])
def add_student():
    # existing upload-based enrollment (webcam or file input)
    if 'image' not in request.files:
        return jsonify({"status": "error", "msg": "No image file provided"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"status": "error", "msg": "No selected file"}), 400

    name = request.form.get('name', '').lower()
    if not name:
        return jsonify({"status": "error", "msg": "No name provided"}), 400

    temp = f"tmp_{time.time()}.jpg"
    try:
        file.save(temp)
        pil_img = Image.open(temp).convert('RGB')
        pil_img.thumbnail((500, 500))
        pil_img.save(temp)
        img = face_recognition.load_image_file(temp)
        with face_lock:
            encs = face_recognition.face_encodings(img)
        if os.path.exists(temp): os.remove(temp)
        if not encs:
            return jsonify({"status": "error", "msg": "No face detected in the image"})
        with data_lock:
            known_names.append(name)
            known_encodings.append(encs[0])
            attendance_log[name] = "Absent"
            with open(FACES_FILE, "wb") as f:
                pickle.dump({"encodings": known_encodings, "names": known_names}, f)
        logger.info(f"Registered: {name}")
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Enrollment error: {e}")
        if os.path.exists(temp):
            try: os.remove(temp)
            except: pass
        return jsonify({"status": "error", "msg": str(e)})


@app.route('/api/start_live_enroll', methods=['POST'])
def start_live_enroll():
    global enroll_mode, enroll_name, attendance_enabled
    data = request.get_json() or {}
    name = data.get('name', '').lower()
    if not name:
        return jsonify({"status": "error", "msg": "No name provided"}), 400
    
    with data_lock:
        enroll_mode = True
        enroll_name = name
        attendance_enabled = False # Stop attendance while enrolling
    
    logger.info(f"Live Enrollment Started for: {name}")
    return jsonify({"status": "success", "msg": f"Waiting for {name}"})

@app.route('/api/cancel_live_enroll', methods=['POST'])
def cancel_live_enroll():
    global enroll_mode, enroll_name, attendance_enabled
    with data_lock:
        enroll_mode = False
        enroll_name = ""
        attendance_enabled = True
    return jsonify({"status": "success"})

@app.route('/api/enroll_status')
def enroll_status():
    global enroll_mode, enroll_name
    return jsonify({"enroll_mode": enroll_mode, "enroll_name": enroll_name})

@app.route('/api/add_student_from_path', methods=['POST'])
def add_student_from_path():
    data = request.get_json() or {}
    name = data.get('name', '').lower()
    path = data.get('path', '')
    if not name:
        return jsonify({"status": "error", "msg": "No name provided"}), 400
    if not path:
        return jsonify({"status": "error", "msg": "No path provided"}), 400
    
    # Security Check: Prevent path traversal
    base_dir = os.path.abspath(os.getcwd())
    target_path = os.path.abspath(path)
    if not target_path.startswith(base_dir):
         # If it's not relative to our app, check if it's a common image dir or just block it.
         # For safety in this context, we'll only allow paths within the workspace.
         return jsonify({"status": "error", "msg": "Access denied to external paths"}), 403

    if not os.path.isfile(target_path):
        return jsonify({"status": "error", "msg": "File does not exist"}), 400

    try:
        img = face_recognition.load_image_file(target_path)
        with face_lock:
            encs = face_recognition.face_encodings(img)
        if not encs:
            return jsonify({"status": "error", "msg": "No face detected in the image"})
        with data_lock:
            if name not in known_names:
                known_names.append(name)
                known_encodings.append(encs[0])
                attendance_log[name] = "Absent"
                with open(FACES_FILE, "wb") as f:
                    pickle.dump({"encodings": known_encodings, "names": known_names}, f)
        logger.info(f"Registered from path: {name} ({path})")
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Enrollment path error: {e}")
        return jsonify({"status": "error", "msg": str(e)})

@app.route('/enroll_frame')
def enroll_frame():
    return render_template('enroll_frame.html')

        
if __name__ == "__main__":
    print("-" * 30)
    print("AURA: LIVE VOCAL SYSTEM ONLINE")
    print(f"VOICE: {VOICE_NAME}")
    print("-" * 30)

    # Vocal confirmation
    def boot_speak():
        time.sleep(1)
        run_speak("AURA system online and vocal core initialized.")
    
    threading.Thread(target=boot_speak, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, threaded=True)
