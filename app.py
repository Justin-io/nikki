import os, time, logging, threading, pickle, random, subprocess, gc, numpy as np
from collections import deque
import cv2, face_recognition
from flask import Flask, render_template, Response, jsonify, request
from picamera2 import Picamera2
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

# --- CAMERA INITIALIZATION (SAFE) ---
picam2 = None
try:
    logger.info("Attempting to initialize camera...")
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"}))
    picam2.start()
    logger.info("Camera initialized successfully.")
except Exception as e:
    logger.error(f"Camera initialization failed: {e}")
    logger.warning("Running without camera. Video feed will show placeholder.")

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
    
    # If camera failed to start, provide a placeholder image
    if not picam2:
        while True:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Camera Unavailable", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            ret, buf = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buf.tobytes() + b'\r\n')
            time.sleep(1)

    while True:
        try:
            frame = picam2.capture_array()
            frame_counter += 1
            
            if frame_counter % 5 == 0:
                small = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
                
                with face_lock:
                    locs = face_recognition.face_locations(small, model="hog")
                    encs = face_recognition.face_encodings(small, locs)
                
                names = []
                x_positions = []
                
                for (t, r, b, l), enc in zip(locs, encs):
                    name = "Unknown"
                    center_x = (l + r) / 2 / 320
                    x_positions.append(center_x)

                    if known_encodings:
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

@app.route('/api/add_student', methods=['POST'])
def add_student():
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
        # FIX: thumbnail returns None, must be called separately
        pil_img = Image.open(file.stream).convert('RGB')
        pil_img.thumbnail((500, 500))
        pil_img.save(temp)
        
        img = face_recognition.load_image_file(temp)
        
        with face_lock: 
            encs = face_recognition.face_encodings(img)
        
        if os.path.exists(temp): os.remove(temp)
        
        if not encs: 
            return jsonify({"status": "error", "msg": "No face detected"})
        
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
        if os.path.exists(temp): os.remove(temp)
        return jsonify({"status": "error", "msg": str(e)})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)
