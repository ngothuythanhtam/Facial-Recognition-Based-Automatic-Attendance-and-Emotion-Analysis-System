import cv2
import os
import numpy as np
import pickle
from deepface import DeepFace

class Extract_Embeddings():
    def __init__(self, rootdir):
        self.dataset_dir = os.path.join(rootdir, 'face-db/DI21V7F1')
        self.face_encodings = []
        self.face_labels = []
        # print("dataset: ",self.dataset_dir)   

    def get_student_details(self):
        details = os.listdir(self.dataset_dir)
        student_details = {}
        for item in details:
            if os.path.isdir(os.path.join(self.dataset_dir, item)):
                student_details[item] = None
        return student_details
    
    def get_remaining_names(self, dictionaries, unique_names):
        remaining_names = np.setdiff1d(list(dictionaries.keys()), unique_names).tolist()
        return remaining_names
    
    def resize_image(self, image, size=(224, 224)):
        """Resize the image to a specific size."""
        return cv2.resize(image, size)

    def get_all_face_pixels(self, dictionaries):
        image_ids = []
        image_paths = []
        image_arrays = []
        names = []
        face_ids = []
        target_size = (224, 224)  # Define the target size for all images

        for category in list(dictionaries.keys()):
            path = os.path.join(self.dataset_dir, category)
            if not os.path.isdir(path):
                print(f"Warning: Directory does not exist: {path}")
                continue
            for img in os.listdir(path):
                img_path = os.path.join(path, img)
                if not os.path.isfile(img_path):
                    print(f"Warning: File does not exist: {img_path}")
                    continue
                if not img_path.lower().endswith('.jpg'):
                    print(f"Warning: Skipping non-JPG file: {img_path}")
                    continue
                try:
                    img_array = cv2.imread(img_path)
                    if img_array is None:
                        print(f"Warning: Unable to read image file: {img_path}")
                        continue
                    img_array_resized = self.resize_image(img_array, target_size)
                    image_paths.append(img_path)
                    image_ids.append(img)
                    image_arrays.append(img_array_resized)
                    names.append(category)
                    face_ids.append(None)  # IDs are not used
                except Exception as e:
                    print(f"Error processing image {img_path}: {e}")

        return [image_ids, image_paths, image_arrays, names, face_ids]

    def get_remaining_face_pixels(self, dictionaries, remaining_names):
        image_ids = []
        image_paths = []
        image_arrays = []
        names = []
        face_ids = []
        for category in remaining_names:
            path = os.path.join(self.dataset_dir, category)
            for img in os.listdir(path):
                img_path = os.path.join(path, img)
                if not os.path.isfile(img_path):
                    print(f"Warning: File does not exist: {img_path}")
                    continue
                if not img_path.lower().endswith('.jpg'):
                    print(f"Warning: Skipping non-JPG file: {img_path}")
                    continue
                try:
                    img_array = cv2.imread(img_path)
                    if img_array is None:
                        print(f"Warning: Unable to read image file: {img_path}")
                        continue
                    image_paths.append(img_path)
                    image_ids.append(img)
                    image_arrays.append(img_array)
                    names.append(category)
                    face_ids.append(None)  # IDs are not used
                except Exception as e:
                    print(f"Error processing image {img_path}: {e}")
        return [image_ids, image_paths, image_arrays, names, face_ids] if image_arrays else None

    def normalize_pixels(self, image_arrays):
        self.image_arrays = image_arrays
        
        # Debug: Print shapes of the image arrays
        for i, img_array in enumerate(self.image_arrays):
            if isinstance(img_array, np.ndarray):
                print(f"Image {i} shape: {img_array.shape}")
            else:
                print(f"Image {i} is not a NumPy array. Type: {type(img_array)}")

        try:
            # Ensure all image arrays are NumPy arrays and have the same shape
            face_pixels = np.array(self.image_arrays)
            # Scale pixel values
            face_pixels = face_pixels.astype('float32')

            # Standardize pixel values across channels (global)
            mean, std = face_pixels.mean(), face_pixels.std()
            face_pixels = (face_pixels - mean) / std

            return face_pixels
        
        except Exception as e:
            print(f"Error normalizing pixels: {e}")
            return None

    def extract_and_save_embeddings(self):
        staff_details = self.get_student_details()
        all_face_pixels = self.get_all_face_pixels(staff_details)
        image_ids, image_paths, image_arrays, names, face_ids = all_face_pixels
        
        # Extract embeddings using DeepFace
        for img_path in image_paths:
            try:
                embedding = DeepFace.represent(img_path=img_path, model_name='Facenet', detector_backend='mtcnn')
                if len(embedding) > 0:
                    self.face_encodings.append(embedding[0]["embedding"])
                    self.face_labels.append(names[image_paths.index(img_path)])
            except Exception as e:
                print(f"Could not extract features from image {img_path}: {e}")

        # Normalize pixels
        normalized_pixels = self.normalize_pixels(image_arrays)
        
        # Save data to a .pkl file
        output_path = os.path.join(self.dataset_dir, 'face_emb.pkl')
        with open(output_path, 'wb') as file:
            pickle.dump({
                'encodings': self.face_encodings,
                'labels': self.face_labels,
                'normalized_pixels': normalized_pixels
            }, file)

        print(f"Successfully saved face data to {output_path}")

rootdir = os.getcwd()  
# rootdir = os.getcwdb().decode('utf-8')
# model_path = rootdir
# extractor = Extract_Embeddings(model_path, rootdir)
extractor = Extract_Embeddings(rootdir)
extractor.extract_and_save_embeddings()