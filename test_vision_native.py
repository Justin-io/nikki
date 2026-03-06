from picamera2 import Picamera2
import cv2
import time

print("Initializing native Picamera2 pipeline...")
try:
    picam2 = Picamera2()
    # Configure for a standard 640x480 resolution to save processing power later
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()

    print("Hardware connected. Warming up sensor...")
    time.sleep(2) # Allow auto-exposure to settle

    # Capture directly into an OpenCV-compatible NumPy array
    frame = picam2.capture_array()

    # Save the frame
    cv2.imwrite("native_vision_test.jpg", frame)
    print("SUCCESS: Frame captured natively and saved as native_vision_test.jpg")

    picam2.stop()
except Exception as e:
    print(f"FATAL: Hardware interaction failed. Error: {e}")
