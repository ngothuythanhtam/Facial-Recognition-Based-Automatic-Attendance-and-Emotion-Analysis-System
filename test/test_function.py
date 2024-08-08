import json
from deepface import DeepFace
import matplotlib.pyplot as plt
import cv2
import dlib
import tensorflow as tf
import numpy as np

metrics = ["cosine", "euclidean", "euclidean_l2"]

# #face verification
# result = DeepFace.verify(
#   img1_path = "img1.jpg", 
#   img2_path = "img2.jpg", 
#   distance_metric = metrics[1],
# )

# #face recognition
# dfs = DeepFace.find(
#   img_path = "img1.jpg", 
#   db_path = "C:/workspace/my_db", 
#   distance_metric = metrics[2],
# )

class_id = 'DI21V7F1'
student_id = 'B2112010'

img1_path = f"D:/NCKH/deepface/face-db/{class_id}/{student_id}/img1.jpg"
img2_path = f"D:/NCKH/deepface/face-db/{class_id}/{student_id}/img10.jpg"
backends = ["opencv", "ssd", "dlib", "mtcnn", "retinaface", "mediapipe"]
models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "SFace","GhostFaceNet"]

def detect_face():
    face = DeepFace.detectFace(img2_path, target_size=(224, 224),detector_backend=backends[3])
    if face is not None:
            # Printing the shape of the 'face' object
            print("Shape of face:", face.shape)
    else:
            print("No face detected.")
    plt.imshow(plt.imread(img2_path))
    plt.show()

def verify_face():
    result = DeepFace.verify(img1_path, img2_path, model_name = models[4], distance_metric = metrics[0],)
    fig, axs = plt.subplots(1, 2, figsize=(10,5))
    axs[0].imshow(plt.imread(img1_path))
    axs[1].imshow(plt.imread(img2_path))
    fig.suptitle(f"Verified: {result['verified']} - Distance: {result['distance']} - Model: {result['model']}")
    plt.show()
    # result = DeepFace.verify(img1_path, img2_path, model_name = models[4], detector_backend=backends[3])
    print(json.dumps(result, indent=2))

def find_face():
    dfs=DeepFace.find(img_path=img1_path, db_path=f'./face-db/DI21V7F1', enforce_detection=False, model_name='VGG-Face')
    print(dfs)

def face_analysis():
    objs = DeepFace.analyze(img_path = "src.jpg", actions = ['age', 'gender', 'race', 'emotion'])
    print(json.dumps(objs, indent=2))

# detect_face()
verify_face()
# find_face()
# face_analysis()