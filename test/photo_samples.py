# import pandas as pd
# import hashlib, binascii, os
# import pymysql

# def hash_password(password):
#     salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
#     password_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
#     password_hash = binascii.hexlify(password_hash)
#     return (salt + password_hash).decode('ascii')

# # Đường dẫn đến file Excel
# file_path = r'D:\NCKH\deepface\db\account.xlsx'
# # Kết nối tới cơ sở dữ liệu
# conn = pymysql.connect(host = 'localhost', user = 'root', password = '', database = 'face_recognition')
# cursor = conn.cursor()

# # Đọc file Excel
# df = pd.read_excel(file_path)

# # Hash các mật khẩu trong cột 'Password'
# df.rename(columns={
#     'Student Code': 'acc_username',
#     'Password': 'acc_password',
#     'Role': 'role_ID'}, inplace=True)

# df['acc_password'] = df['acc_password'].apply(hash_password)
# df['role_ID'] = df['role_ID'].astype(int)

# # Tạo DataFrame mới với các cột cần thiết
# # account_data = df[['student code', 'acc_password', 'role']].copy()
# df = df[['acc_username', 'acc_password', 'role_ID']]

# # Câu lệnh SQL để chèn dữ liệu
# insert_query = """
# INSERT INTO accounts (acc_username, acc_password, role_ID)
# VALUES (%s, %s, %s)
# """

# # Chèn từng hàng dữ liệu vào bảng account
# for index, row in df.iterrows():
#     cursor.execute(insert_query, tuple(row))

# # Lưu các thay đổi vào cơ sở dữ liệu
# conn.commit()
# print('Success')

# # Đóng kết nối
# cursor.close()
# conn.close()

import cv2
import numpy as np
import pickle
import time
from deepface import DeepFace

# Function to load embeddings and labels from pickle file
def load_embeddings(embeddings_file):
    with open(embeddings_file, 'rb') as f:
        embeddings, labels = pickle.load(f)
    return embeddings, labels

# Function to calculate cosine similarity
def cosine_similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

# Function to recognize face in the frame
def recognize_face(frame, embeddings, labels):
    recognized_label = "Unknown"
    try:
        # Extract face embedding using DeepFace
        embedding = DeepFace.represent(img_path=frame, model_name='Facenet')[0]['embedding']
        
        # Compute cosine similarities
        similarities = np.array([cosine_similarity(embedding, e) for e in embeddings])
        
        # Find the label of the most similar embedding
        max_similarity = np.max(similarities)
        if max_similarity > 0.5:  # Adjust similarity threshold as needed
            index = np.argmax(similarities)
            recognized_label = labels[index]
    except Exception as e:
        print(f"Error recognizing face: {e}")
    
    return recognized_label

# Load embeddings and labels
embeddings_file = 'face-db/DI21V7F1/face_data.pkl'
embeddings, labels = load_embeddings(embeddings_file)

# Open the camera
cap = cv2.VideoCapture(0)
recognized_label = "Unknown"
attendance = set()
pTime = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    # Resize frame to speed up processing
    resized_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Recognize face in the frame
    recognized_label = recognize_face(resized_frame, embeddings, labels)
    
    # Mark attendance
    if recognized_label != "Unknown":
        attendance.add(recognized_label)
    
    # Display recognized label and FPS on the frame
    cv2.putText(frame, recognized_label, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    text = f'FPS: {int(fps)}'
    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 3, 2)
    text_width, text_height = text_size

    text_x = frame.shape[1] - text_width - 20
    text_y = text_height + 20

    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
    cv2.imshow('Real-Time Attendance', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Print attendance
print("Attendance:", attendance)
