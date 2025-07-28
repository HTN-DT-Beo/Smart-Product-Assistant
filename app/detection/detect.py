import numpy as np
from ultralytics import YOLO

PT_MODEL_PATH = "app/detection/model/best.pt"

def detect_label(image_path, model_path=PT_MODEL_PATH):
    model = YOLO(model_path)
    results = model(image_path)

    if not results or not results[0].boxes:
        return None

    boxes = results[0].boxes
    best_idx = np.argmax([b.conf[0].item() for b in boxes])
    label_id = int(boxes[best_idx].cls[0].item())

    class_names = model.names
    return class_names[label_id] if label_id in class_names else f"Label {label_id}"
