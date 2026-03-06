import face_recognition
import pickle
import os

known_encodings = []
known_names = []
path = "known_faces/"

print("Encoding HOPE Platform authorized personnel...")

for filename in os.listdir(path):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # Load image and get name from filename
        image = face_recognition.load_image_file(f"{path}{filename}")
        name = os.path.splitext(filename)[0]
        
        # Generate the 128-point encoding
        encoding = face_recognition.face_encodings(image)[0]
        
        known_encodings.append(encoding)
        known_names.append(name)
        print(f"Memorized: {name}")

# Save the memory to a file so we don't have to re-encode every time
with open("trained_faces.pkl", "wb") as f:
    pickle.dump({"encodings": known_encodings, "names": known_names}, f)

print("Memory file 'trained_faces.pkl' created successfully.")
