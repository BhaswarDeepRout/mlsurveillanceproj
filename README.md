This project is an AI-powered surveillance system built with YOLOv8, Tkinter, Flask, and SQLite to monitor a conveyor area.
It detects people in the Region of Interest (ROI), tracks violations when more than 5 persons are present, and provides both a local HMI (Tkinter) and a web-based UI (Flask) for monitoring.

Features:-

>Real-time person detection using YOLOv8;
>Violation monitoring when persons > 5 in ROI;
>Tkinter-based HMI for local monitoring & image upload;
>Flask web app to view stored violation images from the database;
>SQLite database integration for storing violation logs and snapshots;
>Custom YOLO training support for conveyor-specific dataset;

Tech Stack:-

>Machine Learning: YOLOv8 (Ultralytics);
>Database: SQLite;
>Frontend (Local): Tkinter HMI;
>Frontend (Web): Flask + HTML/CSS;
>Backend: Python;
>Image Processing: OpenCV;

Installation:-

Clone the repository:
  >git clone https://github.com/BhaswarDeepRout/mlsurveillanceproj.git

Install dependencies:
  >pip install -r requirements.txt
