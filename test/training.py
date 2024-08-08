from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
import pickle
import numpy as np

class Training:
    def __init__(self, embedding_path):
        self.embedding_path = embedding_path

    def load_embeddings_and_labels(self):
        with open(self.embedding_path, "rb") as file:
            data = pickle.load(file)

        # Encoding labels by names
        label = LabelEncoder()
        ids = np.array(data["face_ids"])                       
        labels = label.fit_transform(ids)

        # Getting embeddings
        embeddings = np.array(data["embeddings"])

        return label, labels, embeddings, ids

    def create_svm_model(self, labels, embeddings):
        model_svc = LinearSVC()
        recognizer = CalibratedClassifierCV(model_svc)
        recognizer.fit(embeddings, labels)
        return recognizer

# Path to the embeddings file
embedding_path = 'embeddings.pkl'

# Instantiate the training class
training_obj = Training(embedding_path)

# Load embeddings and labels
label_encoder, labels, embeddings, ids = training_obj.load_embeddings_and_labels()

# Train the SVM model
svm_model = training_obj.create_svm_model(labels, embeddings)

# Save the trained model and label encoder for later use
with open('svm_model.pkl', 'wb') as model_file:
    pickle.dump(svm_model, model_file)

with open('label_encoder.pkl', 'wb') as label_file:
    pickle.dump(label_encoder, label_file)

print("Model trained and saved successfully.")
