import face_recognition
import cv2
import numpy as np

print("Booting HOPE vision engine with Auto-Exposure Enhancement...")

# 1. Load the image
image = cv2.imread("native_vision_test.jpg")

# 2. Enhance the image (Convert to YUV, equalize the brightness channel, convert back)
img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
enhanced_image = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB) # Convert to RGB for face_recognition

print("Scanning for facial landmarks in enhanced frame...")
face_locations = face_recognition.face_locations(enhanced_image)

if len(face_locations) == 0:
    print("WARNING: Still no face detected. Trying deeper scan...")
    # Fallback: Upsample the image once to find smaller/darker faces
    face_locations = face_recognition.face_locations(enhanced_image, number_of_times_to_upsample=1)

if len(face_locations) > 0:
    print(f"SUCCESS: Locked onto {len(face_locations)} face(s)!")
    cv2_image = cv2.cvtColor(enhanced_image, cv2.COLOR_RGB2BGR)
    for top, right, bottom, left in face_locations:
        cv2.rectangle(cv2_image, (left, top), (right, bottom), (0, 255, 0), 2)
    cv2.imwrite("face_detected_test.jpg", cv2_image)
    print("Result saved as face_detected_test.jpg")
else:
    print("FATAL: Environment too dark. Please illuminate your face directly.")
