import pickle
import numpy as np

# # Path to your pickle file
# pkl_file_path = 'face-db/DI21V7F1/face_data.pkl'

# # Open the pickle file and load data
# with open(pkl_file_path, 'rb') as file:
#     face_encodings, face_labels = pickle.load(file)

# # Print all content in the pickle file
# print("Face Encodings:")
# print(np.array(face_encodings))
# print()

# print("Face Labels:")
# print(np.array(face_labels))

# import pickle

# # Path to the pickle file
# pkl_file_path = 'face-db/DI21V7F1/face_emb.pkl'

# # Open and load the pickle file
# try:
#     with open(pkl_file_path, 'rb') as file:
#         data = pickle.load(file)

#     # Print the type and structure of the loaded data
#     print("Type of loaded data:", type(data))
    
#     # If the data is a tuple or list, print its length and contents
#     if isinstance(data, (tuple, list)):
#         print("Length of data:", len(data))
#         for i, item in enumerate(data):
#             print(f"Item {i} type: {type(item)}")
#             print(f"Item {i} content (first 5 elements if list/array):", item[:5] if len(item) > 5 else item)
#     else:
#         print("Data content:", data)

# except FileNotFoundError:
#     print(f"The file {pkl_file_path} does not exist.")
# except pickle.UnpicklingError:
#     print(f"Error unpickling the file {pkl_file_path}.")
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")

import pickle
import numpy as np

# Path to the pickle file
pkl_file_path = 'embeddings.pkl'

# Open and load the pickle file
try:
    with open(pkl_file_path, 'rb') as file:
        data = pickle.load(file)

    # Print the type and structure of the loaded data
    print("Type of loaded data:", type(data))
    
    # If the data is a dictionary, print its keys and values
    if isinstance(data, dict):
        print("Keys in data:", data.keys())
        for key, value in data.items():
            print(f"Key: {key}, Type: {type(value)}")
            if isinstance(value, (list, np.ndarray)):
                print(f"Value (All elements if list/array):", value)
            else:
                print(f"Value content: {value}")
    else:
        print("Data content:", data)

except FileNotFoundError:
    print(f"The file {pkl_file_path} does not exist.")
except pickle.UnpicklingError:
    print(f"Error unpickling the file {pkl_file_path}.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

