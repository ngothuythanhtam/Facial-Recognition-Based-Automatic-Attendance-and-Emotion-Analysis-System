from matplotlib import pyplot as plt
import time
import cv2
import os
import json

def export():
    data = []
    for folder in os.listdir("./face-db"):
        if folder.startswith("B"):
            folder_path = os.path.join("./face-db", folder)
            images = []
            for file in os.listdir(folder_path):
                if file.endswith(".jpg"):
                    file_path = os.path.join(folder_path, file)
                    images.append(file_path)
            data.append({"Student's ID": folder, "img": images})
    
    with open("face_data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

export()
