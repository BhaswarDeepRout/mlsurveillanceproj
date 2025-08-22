from ultralytics import YOLO
model = YOLO("yolov8x.pt")
model.train(
    data="conveyor.yaml",
    epochs=50,
    imgsz=640,
    batch=8,
    name="conveyor_custom_yolov8"
)
