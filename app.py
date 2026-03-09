import os, time, logging, threading, pickle, random, subprocess, gc, numpy as np
from collections import deque
import cv2, face_recognition
from flask import Flask, render_template, Response, jsonify, request
from PIL import Image

# --- CONFIGURATION ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger("AURA")
app = Flask(__name__)
SERVER_START = time.time()

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
    except: pass

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
    try:
        logger.info("Attempting USB Camera fallback...")
        usb_cam = cv2.VideoCapture(0)
        if not usb_cam.isOpened():
            raise RuntimeError("Cannot open USB camera at index 0")
        
        usb_cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        usb_cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        usb_cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        camera_type = "USB"
        logger.info("SUCCESS: USB Camera initialized.")
    except Exception as e:
        logger.error(f"USB Camera failed: {e}")
        usb_cam = None

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

            with data_lock:
                if t: sensor_cache["temp"] = t
                if h: sensor_cache["hum"] = h
                if mq135: sensor_cache["aqi"] = abs(mq135.value / 32767.0 * 100)
                sensor_cache.update({"cpu": sys_t, "ram": sys_r, "net": sys_n})
                sensor_cache["bat"] = max(0, 100.0 - ((time.time()-SERVER_START)/60*0.05))
        except: pass
        time.sleep(2)

threading.Thread(target=sensor_loop, daemon=True).start()

# --- VISION ENGINE ---
last_locations, last_names = [], []
frame_counter = 0

def gen_frames():
    global last_locations, last_names, frame_counter, scene_data
    
    if not picam2 and not usb_cam:
        while True:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Camera Unavailable", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            ret, buf = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')
            time.sleep(1)

    while True:
        try:
            frame = None
            
            if picam2:
                frame = picam2.capture_array()
            elif usb_cam:
                ret_val, frame = usb_cam.read()
                if not ret_val or frame is None:
                    time.sleep(0.1)
                    continue
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            frame_counter += 1
            
            if frame_counter % 5 == 0:
                small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
                
                with face_lock:
                    locs = face_recognition.face_locations(small, model="hog")
                    encs = face_recognition.face_encodings(small, locs)
                
                names = []
                x_positions = []
                
                for (t, r, b, l), enc in zip(locs, encs):
                    if enroll_mode and enroll_name:
                        # AUTO ENROLLMENT LOGIC
                        with data_lock:
                            name = enroll_name.lower()
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
                            else:
                                # Update encoding if already exists? (Maybe later)
                                pass
                        names.append(name)
                        continue

                    name = "Unknown"
                    center_x = (l + r) / 2 / 320
                    x_positions.append(center_x)

                    if known_encodings and attendance_enabled:
                        with face_lock:
                            matches = face_recognition.compare_faces(known_encodings, enc, 0.5)
                        if any(matches):
                            dist = face_recognition.face_distance(known_encodings, enc)
                            name = known_names[np.argmin(dist)]
                            with data_lock: attendance_log[name] = "Present"
                    names.append(name)
                
                last_locations = [(t*2, r*2, b*2, l*2) for t,r,b,l in locs]
                last_names = names

                with data_lock:
                    scene_data["names"] = names
                    scene_data["count"] = len(names)
                    scene_data["x_pos"] = np.mean(x_positions) if x_positions else 0.5
            
            for (t,r,b,l), name in zip(last_locations, last_names):
                cv2.rectangle(frame, (l,t), (r,b), (255, 255, 255), 2)
                cv2.rectangle(frame, (l,b-30), (r,b), (255, 255, 255), -1)
                cv2.putText(frame, name, (l+6, b-6), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)

            ret, buf = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')
            
        except Exception as e:
            logger.error(f"Frame generation error: {e}")
            time.sleep(0.1)

# --- ROUTES ---
@app.route('/')
def index(): 
    return render_template('index.html')

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

# --- REALISTIC TTS ENDPOINT (Google TTS) ---
@app.route('/api/speak', methods=['POST'])
def api_speak():
    data = request.get_json()
    text = data.get('text', '')
    if text:
        def speak_thread():
            tmp_file = f"/tmp/aura_speech_{time.time()}.mp3"
            try:
                from gtts import gTTS
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(tmp_file)
                subprocess.call(['mpg123', tmp_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                logger.warning(f"gTTS failed, falling back to espeak. Error: {e}")
                subprocess.call(['espeak', '-ven+f5', '-s150', text], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            finally:
                if os.path.exists(tmp_file):
                    try: os.remove(tmp_file)
                    except: pass
        
        threading.Thread(target=speak_thread, daemon=True).start()
        return jsonify({"status": "speaking"})
    return jsonify({"status": "error", "msg": "No text"}), 400

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
    app.run(host='0.0.0.0', port=5000, threaded=True)