import os
import cv2
import numpy as np
from ultralytics import YOLO
from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings



# ----------- STEP 1: Load YOLO model và detect sản phẩm ----------- #
PT_MODEL_PATH = "models/yolov8n/best.pt"
CATALOG_PATH = "data/info/product_catalog_combined.csv"
IMAGE_TEST_PATH = "data/data_train_yolov8/test_img.jpg"

def detect_label(image_path, model_path=PT_MODEL_PATH):
    model = YOLO(model_path)
    results = model(image_path)

    if not results or not results[0].boxes:
        return None

    # Lấy label có độ tin cậy cao nhất
    boxes = results[0].boxes
    best_idx = np.argmax([b.conf[0].item() for b in boxes])
    label_id = int(boxes[best_idx].cls[0].item())

    class_names = model.names  # dict mapping {id: name}
    return class_names[label_id] if label_id in class_names else f"Label {label_id}"

# ----------- STEP 2: Xây dựng RAG (Vector Store) từ PDF ----------- #
def build_vectorstore():
    loader = CSVLoader(file_path=CATALOG_PATH, encoding="utf-8")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embedding)
    return vectorstore

# ----------- STEP 3: Tích hợp RAG + label YOLO ----------- #
def rag_lookup(image_path):
    label = detect_label(image_path)
    if not label:
        print("Không phát hiện sản phẩm trong ảnh.")
        return

    print(f"[✅] Nhãn phát hiện từ ảnh: {label}")

    vectorstore = build_vectorstore()
    results = vectorstore.similarity_search(label, k=3)

    print("\n[🔍] Kết quả tìm được từ Catalog:")
    for idx, doc in enumerate(results):
        print(f"\n--- Kết quả {idx + 1} ---")
        print(doc.page_content)

# ----------- CHẠY THỬ ----------- #
if __name__ == "__main__":
    image_path = IMAGE_TEST_PATH
    rag_lookup(image_path)
