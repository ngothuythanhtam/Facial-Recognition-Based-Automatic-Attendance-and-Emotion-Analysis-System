# # import cv2
# # import dlib
# # import pickle
# # from deepface import DeepFace
# # import numpy as np
# # import threading
# # import time

# # # Initialize dlib's face detector (HOG-based)
# # detector = dlib.get_frontal_face_detector() # type: ignore

# # # Open the camera
# # cap = cv2.VideoCapture(0)

# # face_locations = []
# # face_encodings = []
# # face_labels = []
# # s = True

# # pkl_file_path = 'face-db/DI21V7F1/face_data.pkl'

# # with open(pkl_file_path, 'rb') as file:
# #     face_encodings, face_labels = pickle.load(file)
    
# # def cosine_similarity(embedding1, embedding2):
# #     return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

# # # Function to get face embedding from image
# # def get_face_embedding(image):
# #     try:
# #         embedding = DeepFace.represent(img_path=image, model_name='DeepFace', detector_backend='mtcnn')
# #         if embedding is not None and len(embedding) > 0:
# #             return embedding[0]["embedding"]
# #         else:
# #             return None
# #     except Exception as e:
# #         print(f"Error extracting embedding: {e}")
# #         return None
    
# # # Function to recognize faces
# # def recognize_faces(frame, face_encodings, face_labels, callback):
# #     recognized_label = "Unknown"
    
# #     try:
# #         faces = DeepFace.extract_faces(frame, detector_backend='mtcnn')
# #         # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# #         # # Detect faces
# #         # faces = detector(gray)
        
# #         if faces is not None and len(faces) > 0:
# #             face_embedding = get_face_embedding(frame)
            
# #             if face_embedding is not None:
# #                 similarities = [cosine_similarity(face_embedding, known_embedding) for known_embedding in face_encodings]
# #                 max_similarity = max(similarities)
                
# #                 if max_similarity > 0.5:  # Adjust similarity threshold as needed
# #                     max_index = similarities.index(max_similarity)
# #                     recognized_label = face_labels[max_index]
# #                 else:
# #                     recognized_label = "Unknown"
# #     except Exception as e:
# #         print(f"Error recognizing faces: {e}")
    
# #     callback(recognized_label)


# # # Variable to keep track of processing state
# # processing = False

# # # Function to process each frame
# # def process_frame(frame):
# #     global processing
# #     if not processing:
# #         processing = True
# #         threading.Thread(target=recognize_faces, args=(frame, face_encodings, face_labels, update_recognized_label)).start()

# # # Callback to update the recognized label
# # def update_recognized_label(label):
# #     global recognized_label, processing
# #     recognized_label = label
# #     processing = False


# # # Main loop for real-time face recognition
# # cap = cv2.VideoCapture(0)
# # recognized_label = "Unknown"
# # pTime = 0

# # while True:
# #     ret, frame = cap.read()
# #     if not ret:
# #         print("Error: Failed to capture image")
# #         break
# #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# #     # Detect faces
# #     faces = detector(gray)
    
# #     for face in faces:
# #             x, y, w, h = face.left(), face.top(), face.width(), face.height()
# #             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
# #             # x, y, w, h = face['facial_area']['x'], face['facial_area']['y'], face['facial_area']['w'], face['facial_area']['h']
# #             # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
# #     process_frame(frame)
    
# #     # Display recognized label and FPS
# #     cv2.putText(frame, recognized_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
# #     cTime = time.time()
# #     fps = 1 / (cTime - pTime)
# #     pTime = cTime
# #     text = f'FPS: {int(fps)}'
# #     text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 3, 2)
# #     text_width, text_height = text_size

# #     text_x = frame.shape[1] - text_width - 20
# #     text_y = text_height + 20

# #     cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
# #     cv2.imshow('Real-Time Face Recognition', frame)
    
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # cap.release()
# # cv2.destroyAllWindows()

# # import os
# # import pickle
# # from deepface import DeepFace

# # # Folder containing student images
# # student_folder = './face-db/DI21V7F1'

# # # List to hold encodings and labels
# # data = []

# # # Process each student image and get its encoding
# # for root, dirs, files in os.walk(student_folder):
# #     for filename in files:
# #         if filename.endswith('.jpg') or filename.endswith('.png'):
# #             student_image_path = os.path.join(root, filename)
# #             label = os.path.basename(root)  # Use the folder name as the label
# #             encoding = DeepFace.represent(img_path=student_image_path, model_name='Facenet', enforce_detection=False)[0]['embedding']
# #             data.append({"label": label, "encoding": encoding})

# # # Save encodings and labels to a file
# # with open('emb.pkl', 'wb') as f:
# #     pickle.dump(data, f)

# # print("Encodings and labels saved to emb.pkl")

# # import pickle

# # # Load encodings and labels from the file
# # with open('./emb.pkl', 'rb') as f:
# #     data = pickle.load(f)

# # # Print the contents of the .pkl file
# # for entry in data:
# #     print(f"Label: {entry['label']}")
# #     print(f"Encoding: {entry['encoding']}\n")

# import cv2
# import pickle
# from deepface import DeepFace
# import numpy as np

# # Load encodings and labels from the file
# with open('emb.pkl', 'rb') as f:
#     data = pickle.load(f)

# # Function to find the best match for a given encoding
# def find_best_match(test_encoding, data):
#     best_match = None
#     best_distance = float('inf')
#     for entry in data:
#         label = entry["label"]
#         encoding = entry["encoding"]
#         distance = np.linalg.norm(np.array(encoding) - np.array(test_encoding))
#         if distance < best_distance:
#             best_distance = distance
#             best_match = label
#     return best_match, best_distance

# # Open webcam
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     try:
#         # Try different detector backends if necessary
#         detected_face = DeepFace.detectFace(frame, detector_backend='mtcnn', enforce_detection=False)
        
#         if detected_face is not None and isinstance(detected_face, dict) and 'region' in detected_face:
#             face_region = detected_face['region']
#             # Draw rectangle around the detected face
#             cv2.rectangle(frame, (face_region['x'], face_region['y']),
#                           (face_region['x'] + face_region['w'], face_region['y'] + face_region['h']), (255, 0, 255), 2)

#             # Encode face
#             test_encoding = DeepFace.represent(img_path=frame, model_name='Facenet', enforce_detection=False)[0]['embedding']

#             # Find the best match
#             best_match, best_distance = find_best_match(test_encoding, data)

#             # Display the best match result
#             if best_match:
#                 cv2.putText(frame, f'{best_match} {round(best_distance, 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
#         else:
#             print("No face detected or incorrect detection output.")

#     except Exception as e:
#         print(f"Error: {e}")

#     # Show the frame
#     cv2.imshow('Real-Time Face Recognition', frame)

#     # Break the loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()

import cv2
import dlib
import pickle
from deepface import DeepFace
import numpy as np
import threading
import time
import os

# Initialize dlib's face detector (HOG-based)
detector = dlib.get_frontal_face_detector() # type: ignore

# Function to calculate Euclidean distance between two vectors
def euclidean_distance(vector1, vector2):
    return np.linalg.norm(np.array(vector1) - np.array(vector2))

# Function to find the best match for a given face encoding
def find_best_match(test_encoding, data):
    best_match = None
    best_distance = float('inf')
    for encoding, label in zip(*data):
        distance = euclidean_distance(encoding, test_encoding)
        if distance < best_distance:
            best_distance = distance
            best_match = label
    return best_match, best_distance

# Function to get face embedding from image
def get_face_embedding(image):
    try:
        embedding = DeepFace.represent(img_path=image, model_name='DeepFace', detector_backend='mtcnn', enforce_detection=False)
        if embedding is not None and len(embedding) > 0:
            return embedding[0]["embedding"]
        else:
            return None
    except Exception as e:
        print(f"Error extracting embedding: {e}")
        return None

# Function to recognize faces
def recognize_faces(frame, data):
    recognized_labels = []
    
    try:
        # Detect faces
        faces = DeepFace.extract_faces(frame, detector_backend='mtcnn', enforce_detection=False)
        
        for face in faces:
            face_embedding = get_face_embedding(face['face'])
            if face_embedding is not None:
                best_match, best_distance = find_best_match(face_embedding, data)
                if best_distance < 0.6:  # Adjust the threshold as needed
                    recognized_label = best_match
                else:
                    recognized_label = "Unknown"
                
                recognized_labels.append((recognized_label, face['facial_area']))
    
    except Exception as e:
        print(f"Error recognizing faces: {e}")
    
    return recognized_labels

# Load face encodings and labels
pkl_file_path = './face-db/DI21V7F1/face_data.pkl'
with open(pkl_file_path, 'rb') as file:
    face_encodings, face_labels = pickle.load(file)

# Main loop for real-time face recognition
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video capture")
    exit()

recognized_label = "Unknown"
pTime = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break
    
    recognized_labels = recognize_faces(frame, (face_encodings, face_labels))
    
    for label, rect in recognized_labels:
        x, y, w, h = rect['x'], rect['y'], rect['w'], rect['h']
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    # Display FPS
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
