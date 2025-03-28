# Student Attendance and Emotion Analysis System

This project is a **Student Attendance and Emotion Analysis System** that leverages facial recognition and emotion detection to streamline attendance and assess student engagement based on facial expressions. The system utilizes DeepFace for face detection, recognition, and emotion analysis, and offers a web interface to view attendance and emotion reports.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [License](#license)

## Overview

The system supports automatic face detection and recognition to mark attendance, along with emotion analysis to gauge students' engagement levels in real-time. It uses:

- **DeepFace** library for facial recognition and emotion analysis (Reference: https://github.com/serengil/deepface)
- **MySQL** for storing face data and attendance records
- **Tkinter** and **Django** for the GUI system and web interface

## Features

1. **Face Detection**: Uses RetinaFace for robust face detection in varying lighting and angles.
2. **Face Recognition**: Employs models like ArcFace to accurately map faces to feature vectors and compare them.
3. **Emotion Analysis**: Analyzes students' facial expressions using DeepFace to categorize emotions such as happy, sad, angry, surprised, and neutral.
4. **Database Integration**: Stores face data, attendance, and emotion analysis results in a MySQL database for fast retrieval and reporting.
5. **Report Generation**: Web interface for viewing detailed reports on attendance and emotion analysis by class and course.

## System Architecture

The system architecture is divided into:

- **Face Detection and Recognition**: Captures and identifies faces using RetinaFace and ArcFace models.
- **Emotion Analysis**: Classifies emotions based on facial expressions using DeepFace.
- **Database Management**: Stores attendance, student profiles, and emotion data in MySQL.
- **Web Interface**: Allows teachers and students to view attendance records and emotion analysis.

## Installation

### Prerequisites

- Python >=3.9 (We use Python 3.9.6 version)
- MySQL Server
- Required Python packages (see `requirements.txt`)

### How to run

1. Clone the repository:
   ```bash
   git clone https://github.com/ngothuythanhtam/Facial-Recognition-Based-Automatic-Attendance-and-Emotion-Analysis-System.git
   cd Facial-Recognition-Based-Automatic-Attendance-and-Emotion-Analysis-System
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


