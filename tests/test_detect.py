# import cv2
# import numpy as np
# import os
# from ultralytics import YOLO

# # Đường dẫn file
# onnx_model_path = "models/yolov8n/best.onnx"
# image_path = "data/data_train_yolov8/test_img.jpg"

# # Kiểm tra sự tồn tại của file
# if not os.path.exists(image_path):
#     raise FileNotFoundError(f"Không tìm thấy ảnh: {image_path}")
# if not os.path.exists(onnx_model_path):
#     raise FileNotFoundError(f"Không tìm thấy model ONNX: {onnx_model_path}")

# # Load the exported ONNX model
# onnx_model = YOLO(onnx_model_path)

# # Run inference
# results = onnx_model(image_path)

# for box in results[0].boxes:
#     class_id = int(box.cls[0].item())
#     confidence = float(box.conf[0].item())
#     print(f"Class ID: {class_id}, Confidence: {confidence:.2f}")


from ultralytics import YOLO
import cv2

onnx_model_path = "models/yolov8n/best.onnx"
pt_model_path = "models/yolov8n/best.pt"
image_path = "data/data_train_yolov8/test_img.jpg"

# Load YOLO model (đã train từ Roboflow/CVAT)
model = YOLO(pt_model_path)  # Replace bằng path model của bạn

# Dự đoán ảnh
image = cv2.imread(image_path)
results = model(image)

# Lấy label và toạ độ bbox
for r in results:
    boxes = r.boxes
    for box in boxes:
        label = model.names[int(box.cls)]
        conf = float(box.conf)
        print("Detected:", label, "Confidence:", conf)