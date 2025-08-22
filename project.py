import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO
import sqlite3
import os
import uuid
from flask import Flask, render_template_string
import threading
import numpy as np
model = YOLO('detect/best.pt')
db_path = 'violations.db'
save_folder = 'static/violations'
app = Flask(__name__)
@app.route("/")
def index():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM violations")
    data = cursor.fetchall()
    conn.close()
    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Violation Results for Surveillance System</title>
            <style>
                body {
                    font-family: sans-serif;
                    padding: 20px;
                    background-color: #fff;
                }
                h1 {
                    text-align: center;
                }
                .container {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    justify-content: center;
                }
                .card {
                    border: 1px solid #ccc;
                    background: #fff;
                    width: 220px;
                    padding: 10px;
            </style>
        </head>
        <body>
            <h1>Violation Results for Surveillance System</h1>
            <div class="container">
                {% for row in data %}
                    <div class="card">
                        <img src="/static/violations/{{ row[1] }}" alt="Violation Image">
                        <p><b>Filename:</b> {{ row[1] }}</p>
                        <p><b>Coords:</b> ({{ row[2] }}, {{ row[3] }}) to ({{ row[4] }}, {{ row[5] }})</p>
                    </div>
                {% endfor %}
            </div>
        </body>
        </html>
    ''', data=data)
def run_flask():
    app.run(port=5000, debug=False)
def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS violations (id TEXT PRIMARY KEY, filename TEXT,"
                   " x1 INTEGER, y1 INTEGER, x2 INTEGER, y2 INTEGER)")
    conn.commit()
    conn.close()
def save_violation(image, bbox):
    uid = str(uuid.uuid4())
    x1, y1, x2, y2 = bbox
    crop = image[y1:y2, x1:x2]
    filename = f"{uid}.jpg"
    filepath = os.path.join(save_folder, filename)
    cv2.imwrite(filepath, crop)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO violations VALUES (?, ?, ?, ?, ?, ?)", (uid, filename, x1, y1, x2, y2))
    conn.commit()
    conn.close()
def point_in_polygon(x, y, polygon):
    return cv2.pointPolygonTest(polygon, (x, y), False) >= 0
def detect_persons(img_path):
    img = cv2.imread(img_path)
    results = model(img)[0]
    person_count = 0
    roi_poly = np.array([[812,2],[981,2],[910,718],[532,718]], np.int32)
    img_draw = img.copy()
    for box in results.boxes:
        cls = int(box.cls[0])
        if cls == 0:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            if point_in_polygon(cx, cy, roi_poly):
                person_count += 1
                cv2.rectangle(img_draw, (x1, y1), (x2, y2), (0, 255, 0), 2)
                if person_count > 5:
                    save_violation(img, (x1, y1, x2, y2))
    return img_draw, person_count
def roi_overlay(img):
    overlay = img.copy()
    roi_polygon = np.array([[812,2],[981,2],[910,718],[532,718]], np.int32)
    cv2.fillPoly(overlay, [roi_polygon], (255, 255, 0))
    alpha = 0.3
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
def display_image(cv_img):
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(cv_img)
    img_tk = ImageTk.PhotoImage(img_pil)
    panel.config(image=img_tk)
    panel.image = img_tk
def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        result_img, count = detect_persons(file_path)
        roi_overlay(result_img)
        display_image(result_img)
        status_label['text'] = f"Persons detected: {count}"
init_db()
flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()
root = tk.Tk()
root.title("Intelligent Surveillance System")
root.geometry("800x600")
upload_btn = tk.Button(root, text="Upload Image", command=upload_image, bg="skyblue", font=('Arial', 14))
upload_btn.pack(pady=10)
panel = tk.Label(root)
panel.pack()
status_label = tk.Label(root, text="", font=("Arial", 14), fg="green")
status_label.pack(pady=10)
root.mainloop()