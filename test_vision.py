import cv2
import time

print("Initializing camera pipeline...")
# 0 is usually the default V4L2 hardware node
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("FATAL: OpenCV could not connect to the camera.")
else:
    print("Hardware connection established. Warming up sensor...")
    time.sleep(2) # Give the sensor time to adjust light levels

    ret, frame = cap.read()

    if ret:
        # Save the frame instead of displaying it, avoiding SSH GUI crashes
        cv2.imwrite("vision_test.jpg", frame)
        print("SUCCESS: Frame captured and saved as vision_test.jpg")
    else:
        print("ERROR: Connected to camera, but could not read a frame.")

cap.release()
