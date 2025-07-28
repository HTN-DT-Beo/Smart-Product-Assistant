from app.rag import query_rag

def run_agent():
    # Đường dẫn ảnh test
    image_path = "data/data_train_yolov8/test_img.jpg"
    query_rag.rag_pipeline(image_path)

if __name__ == "__main__":
    run_agent()
