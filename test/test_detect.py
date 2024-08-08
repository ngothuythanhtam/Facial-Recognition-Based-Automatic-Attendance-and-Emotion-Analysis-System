import cv2
import pickle
import csv
from deepface import DeepFace
import numpy as np
import threading
import time
import dlib
from datetime import datetime

detector = dlib.get_frontal_face_detector()  # type: ignore

# Load data from pickle file
pkl_file_path = './face-db/DI21V7F1/face_data.pkl'
csv_file_path = './attendance.csv'

with open(pkl_file_path, 'rb') as file:
    face_encodings, face_labels = pickle.load(file)

def cosine_similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

# Function to get face embedding from image
def get_face_embedding(image):
    try:
        embedding = DeepFace.represent(img_path=image, model_name='DeepFace', detector_backend='mtcnn')
        if embedding is not None and len(embedding) > 0:
            return embedding[0]["embedding"]
        else:
            return None
    except Exception as e:
        print(f"Error extracting embedding: {e}")
        return None

# Function to recognize faces
def recognize_faces(frame, face_encodings, face_labels, callback):
    recognized_label = "Unknown"
    
    try:
        faces = DeepFace.extract_faces(frame, detector_backend='mtcnn')
        
        if faces is not None and len(faces) > 0:
            face_embedding = get_face_embedding(frame)
            
            if face_embedding is not None:
                similarities = [cosine_similarity(face_embedding, known_embedding) for known_embedding in face_encodings]
                max_similarity = max(similarities)
                
                if max_similarity > 0.5:  # Adjust similarity threshold as needed
                    max_index = similarities.index(max_similarity)
                    recognized_label = face_labels[max_index]
                    
    except Exception as e:
        print(f"Error recognizing faces: {e}")
    
    callback(recognized_label)

# Variable to keep track of processing state
processing = False

# Function to process each frame
def process_frame(frame):
    global processing
    if not processing:
        processing = True
        threading.Thread(target=recognize_faces, args=(frame, face_encodings, face_labels, update_recognized_label)).start()

# Function to mark attendance to CSV
def mark_attendance(label):
    with open(csv_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([label, time_now])

# Callback to update the recognized label
def update_recognized_label(label):
    global recognized_label, processing
    recognized_label = label
    if label != "Unknown":
        mark_attendance(label)
    processing = False

# Main loop for real-time face recognition
cap = cv2.VideoCapture(0)
recognized_label = "Unknown"
pTime = 0
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break
    frame = cv2.resize(frame, (640, 480))
    frame_count += 1

    if frame_count % 30 == 0:  # Process every 30th frame
        process_frame(frame)
    
    # process_frame(frame)
    # Convert the frame to grayscale (dlib works with grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = detector(gray)
    # faces = DeepFace.extract_faces(frame, detector_backend='mtcnn', enforce_detection=False)

    # Draw rectangles around detected faces
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(frame, recognized_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    text = f'FPS: {int(fps)}'
    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 3, 2)
    text_width, text_height = text_size

    text_x = frame.shape[1] - text_width - 20
    text_y = text_height + 20

    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
    cv2.imshow('Real-Time Face Recognition', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


