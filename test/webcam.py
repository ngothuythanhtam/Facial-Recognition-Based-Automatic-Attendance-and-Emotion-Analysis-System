# import pickle
# import cv2
# from deepface import DeepFace
# from scipy.spatial.distance import cosine

# # Step 1: Load the Encodings and Labels
# with open('./face-db/DI21V7F1/face_data.pkl', 'rb') as f:
#     face_encodings, face_labels = pickle.load(f)

# # Step 2: Capture Frame from Camera
# video_capture = cv2.VideoCapture(0)
# ret, frame = video_capture.read()

# # Step 3: Extract Features from the Detected Faces using DeepFace
# harcascadePath = "./models/haarcascade_frontalface_default.xml"
# face_cascade = cv2.CascadeClassifier(harcascadePath)
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# face_encodings_in_frame = []
# for (x, y, w, h) in faces:
#     roi_color = frame[y:y+h, x:x+w]
#     try:
#         embedding = DeepFace.represent(roi_color, model_name='DeepFace', enforce_detection=False)[0]['embedding']
#         face_encodings_in_frame.append(embedding)
#     except ValueError as e:
#         print(f"Error processing face at location {(x, y, w, h)}: {e}")

# # Step 4: Compare with Stored Encodings
# def find_best_match(encoding, known_encodings, known_labels):
#     similarities = [1 - cosine(encoding, known_encoding) for known_encoding in known_encodings]
#     best_match_index = similarities.index(max(similarities))
#     return known_labels[best_match_index], max(similarities)

# threshold = 0.6  # Define a threshold for a positive match

# for encoding in face_encodings_in_frame:
#     label, similarity = find_best_match(encoding, face_encodings, face_labels)
#     if similarity > threshold:
#         print(f"Recognized {label} with similarity {similarity:.2f}")
#     else:
#         print("Unknown face detected")

# # Step 5: Display the Results
# for (x, y, w, h), encoding in zip(faces, face_encodings_in_frame):
#     label, similarity = find_best_match(encoding, face_encodings, face_labels)
#     if similarity > threshold:
#         label_text = f"{label} ({similarity:.2f})"
#     else:
#         label_text = "Unknown"

#     # Draw a box around the face
#     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

#     # Draw a label with the name below the face
#     cv2.rectangle(frame, (x, y + h - 35), (x + w, y + h), (0, 0, 255), cv2.FILLED)
#     font = cv2.FONT_HERSHEY_DUPLEX
#     cv2.putText(frame, label_text, (x + 6, y + h - 6), font, 0.5, (255, 255, 255), 1)

# # Display the resulting image
# cv2.imshow('Video', frame)

# # Release the camera
# video_capture.release()
# cv2.destroyAllWindows()

# # import cv2

# # # Open the camera
# # cap = cv2.VideoCapture(0)

# # if not cap.isOpened():
# #     print("Error: Could not open camera.")
# #     exit()

# # while True:
# #     # Capture frame-by-frame
# #     ret, frame = cap.read()
# #     if not ret:
# #         print("Error: Failed to capture image")
# #         break

# #     # Display the resulting frame
# #     cv2.imshow('Camera Feed', frame)

# #     # Break the loop on 'q' key press
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # # Release the camera and close windows
# # cap.release()
# # cv2.destroyAllWindows()

import cv2
import dlib
from deepface import DeepFace

# Initialize dlib's face detector (HOG-based)
detector = dlib.get_frontal_face_detector() # type: ignore

# Open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    # Convert the frame to grayscale (dlib works with grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = detector(gray)
    # faces = DeepFace.extract_faces(frame, detector_backend='mtcnn', enforce_detection=False)

    # Draw rectangles around detected faces
    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # x, y, w, h = face['facial_area']['x'], face['facial_area']['y'], face['facial_area']['w'], face['facial_area']['h']
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Camera Feed', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
