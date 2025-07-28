from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import shutil
import uuid
import os

app = FastAPI()

# Load YOLOv8 model
model = YOLO("app/detection/model/best.pt")

@app.post("/detect")
async def detect_label(image: UploadFile = File(...)):
    try:
        # Lưu ảnh tạm thời
        temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Detect
        results = model(temp_filename)
        labels = results[0].names
        boxes = results[0].boxes
        class_ids = boxes.cls.tolist()

        # Trích nhãn duy nhất (nếu có)
        unique_labels = list(set([labels[int(cls_id)] for cls_id in class_ids]))

        # Xoá ảnh tạm
        os.remove(temp_filename)

        if unique_labels:
            return JSONResponse(content={"labels": unique_labels}, status_code=200)
        else:
            return JSONResponse(content={"labels": []}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# from fastapi import FastAPI
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from ultralytics import YOLO
# import requests
# import uuid
# import os

# app = FastAPI()

# # Load YOLOv8 model
# model = YOLO("app/detection/model/best.pt")

# # Dữ liệu đầu vào chứa URL ảnh
# class ImageInput(BaseModel):
#     image_url: str

# @app.post("/detect")
# async def detect_label(data: ImageInput):
#     try:
#         # Tải ảnh từ URL
#         response = requests.get(data.image_url)
#         if response.status_code != 200:
#             return JSONResponse(content={"error": "Không thể tải ảnh từ URL"}, status_code=400)

#         # Lưu ảnh tạm thời
#         temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
#         with open(temp_filename, "wb") as f:
#             f.write(response.content)

#         # Detect bằng YOLO
#         results = model(temp_filename)
#         labels = results[0].names
#         boxes = results[0].boxes
#         class_ids = boxes.cls.tolist()

#         unique_labels = list(set([labels[int(cls)] for cls in class_ids]))

#         os.remove(temp_filename)

#         return JSONResponse(content={"labels": unique_labels}, status_code=200)

#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)
