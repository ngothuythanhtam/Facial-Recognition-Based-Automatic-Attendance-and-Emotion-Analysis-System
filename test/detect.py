import pickle
import cv2
from deepface import DeepFace
import numpy as np
import pickle
import time

# Load data from pickle file
pkl_file_path = 'face-db/DI21V7F1/face_data.pkl'

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

# Function to recognize faces in real-time
def recognize_faces(frame, face_encodings, face_labels):
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
    return recognized_label

# Main loop for real-time face recognition
# cap = cv2.VideoCapture("http://192.168.1.3:8080/video")  # Adjust camera index as needed
cap = cv2.VideoCapture(0)
pTime = 0
while True:
    ret, frame = cap.read()
    resized = cv2.resize(frame, (600,400))
    if not ret:
        print("Error: Failed to capture image")
        break
    
    recognized_label = recognize_faces(frame, face_encodings, face_labels)
    cv2.putText(frame, recognized_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cTime = time.time()
    fps = 1/(cTime-pTime)
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
