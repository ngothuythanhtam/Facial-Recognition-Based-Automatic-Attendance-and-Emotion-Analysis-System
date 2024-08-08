import os
from deepface import DeepFace
import numpy as np
import pickle

# The root folder contains all student folders
root_folder = "face-db/DI21V7F1"

# Array to store facial features and labels
face_encodings = []
face_labels = []

# Browse all subfolders in the root folder
for student_folder in os.listdir(root_folder):
    student_path = os.path.join(root_folder, student_folder)
    
    # Check if student_path is a directory
    if os.path.isdir(student_path):  
        
        # Browse all files in the student folder
        for image_file in os.listdir(student_path):
            image_path = os.path.join(student_path, image_file)
            try:
                # Extract facial features using Facenet with backend MTCNN
                embedding = DeepFace.represent(img_path=image_path, model_name='Facenet', detector_backend='mtcnn')
                
                if len(embedding) > 0:
                    face_encodings.append(embedding[0]["embedding"])
                    face_labels.append(student_folder)  # Lưu nhãn là tên thư mục sinh viên
            except Exception as e:
                print(f"Unable to extract features from images {image_path}: {e}")

# Convert arrays to numpy arrays
face_encodings = np.array(face_encodings, dtype=object)
face_labels = np.array(face_labels)

# Full path of the .pkl file in the DI21V7F1 folder
output_path = os.path.join(root_folder, 'face_data.pkl')

# Save data to .pkl file
with open(output_path, 'wb') as file:
    pickle.dump((face_encodings, face_labels), file)

print(f"Face data has been successfully stored {output_path}")
