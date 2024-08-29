# common dependencies
import os
import warnings
import logging
from typing import Any, Dict, List, Union, Optional

# this has to be set before importing tensorflow
os.environ["TF_USE_LEGACY_KERAS"] = "1"

# pylint: disable=wrong-import-position

# 3rd party dependencies
import numpy as np
import pandas as pd
import tensorflow as tf

# package dependencies
from deepface.commons import package_utils, folder_utils
from deepface.commons.logger import Logger
from deepface.modules import (
    modeling,
    representation,
    verification,
    recognition,
    demography,
    detection,
    streaming,
    preprocessing,
)

import webcam as video
import phone as phone
import files as files

from deepface import __version__

logger = Logger()

def stream(
    db_path: str,
    model_name: str = "VGG-Face",
    detector_backend: str = "opencv",
    distance_metric: str = "cosine",
    enable_face_analysis: bool = True,
    source: Any = 0,
    time_threshold: int = 3,
    frame_threshold: int = 3,
    anti_spoofing: bool = False,
) -> None:
    """
    Run real time face recognition and facial attribute analysis

    Args:
        db_path (string): Path to the folder containing image files. All detected faces
            in the database will be considered in the decision-making process.

        model_name (str): Model for face recognition. Options: VGG-Face, Facenet, Facenet512,
            OpenFace, DeepFace, DeepID, Dlib, ArcFace, SFace and GhostFaceNet (default is VGG-Face).

        detector_backend (string): face detector backend. Options: 'opencv', 'retinaface',
            'mtcnn', 'ssd', 'dlib', 'mediapipe', 'yolov8', 'centerface' or 'skip'
            (default is opencv).

        distance_metric (string): Metric for measuring similarity. Options: 'cosine',
            'euclidean', 'euclidean_l2' (default is cosine).

        enable_face_analysis (bool): Flag to enable face analysis (default is True).

        source (Any): The source for the video stream (default is 0, which represents the
            default camera).

        time_threshold (int): The time threshold (in seconds) for face recognition (default is 5).

        frame_threshold (int): The frame threshold for face recognition (default is 5).

        anti_spoofing (boolean): Flag to enable anti spoofing (default is False).
    Returns:
        None
    """

    time_threshold = max(time_threshold, 1)
    frame_threshold = max(frame_threshold, 1)
    print("Indexing "+db_path)

    video.analysis(
        db_path=db_path,
        model_name=model_name,
        detector_backend=detector_backend,
        distance_metric=distance_metric,
        enable_face_analysis=enable_face_analysis,
        source=source,
        time_threshold=time_threshold,
        frame_threshold=frame_threshold,
        anti_spoofing=anti_spoofing,
    )

   

def fromfiles(
    db_path: str,
    source_dir: str,
    dest_dir: str,
    model_name: str = "VGG-Face",
    detector_backend: str = "opencv",
    distance_metric: str = "cosine",
    enable_face_analysis: bool = True,
    anti_spoofing: bool = False,
) -> None:
    """
    Run real time face recognition and facial attribute analysis

    Args:
        db_path (string): Path to the folder containing image files. All detected faces
            in the database will be considered in the decision-making process.

        model_name (str): Model for face recognition. Options: VGG-Face, Facenet, Facenet512,
            OpenFace, DeepFace, DeepID, Dlib, ArcFace, SFace and GhostFaceNet (default is VGG-Face).

        detector_backend (string): face detector backend. Options: 'opencv', 'retinaface',
            'mtcnn', 'ssd', 'dlib', 'mediapipe', 'yolov8', 'centerface' or 'skip'
            (default is opencv).

        distance_metric (string): Metric for measuring similarity. Options: 'cosine',
            'euclidean', 'euclidean_l2' (default is cosine).

        enable_face_analysis (bool): Flag to enable face analysis (default is True).

        source (Any): The source for the video stream (default is 0, which represents the
            default camera).

        time_threshold (int): The time threshold (in seconds) for face recognition (default is 5).

        frame_threshold (int): The frame threshold for face recognition (default is 5).

        anti_spoofing (boolean): Flag to enable anti spoofing (default is False).
    Returns:
        None
    """

    print("Indexing "+db_path)

    files.analysis(
        db_path=db_path,
        source_dir=source_dir,
        dest_dir=dest_dir,
        model_name=model_name,
        detector_backend=detector_backend,
        distance_metric=distance_metric,
        enable_face_analysis=enable_face_analysis,
        anti_spoofing=anti_spoofing,
    ) 

# db_path="face-db"
# source_path="test2"
# dest_path="result/face_analysis"
# models = [
#   "VGG-Face", 
#   "Facenet", 
#   "Facenet512", 
#   "OpenFace", 
#   "DeepFace", 
#   "DeepID", 
#   "ArcFace", 
#   "Dlib", 
#   "SFace",
#   "GhostFaceNet",
# ]

# metrics = ["cosine", "euclidean", "euclidean_l2"]

# backends = [
#   'opencv',  
#   'dlib', 
#   'mtcnn', 
#   'retinaface'
# ]
# stream(db_path=db_path, enable_face_analysis=False, model_name="ArcFace", detector_backend="retinaface", anti_spoofing=False,source=0) 
#Theo dõi trạng thái cảm xúc set enable_face_analysis=True, 15s chụp cảm xúc, thống kê bao nhiêu khuôn mặt

# fromfiles(db_path=db_path, source_dir=source_path, dest_dir=dest_path, enable_face_analysis=False, model_name="Facenet", detector_backend="opencv", anti_spoofing=False)
# fromfiles(db_path=db_path, source_dir=source_path, dest_dir=dest_path, enable_face_analysis=True, model_name="ArcFace", detector_backend="retinaface", anti_spoofing=False)