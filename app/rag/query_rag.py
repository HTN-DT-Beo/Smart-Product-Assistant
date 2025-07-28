from app.detection.detect import detect_label
from app.rag.index_documents import build_vectorstore
from app.llm.generate import rag_generate_answer

def rag_pipeline(image_path):
    label = detect_label(image_path)
    if not label:
        print("[❌] Không phát hiện được sản phẩm trong ảnh.")
        return

    print(f"[✅] Nhãn phát hiện: {label}")

    # Tạo câu hỏi rõ ràng từ label
    question = f"""What is the "Giá hiện tại" of the {label}?"""

    vectorstore = build_vectorstore()
    print("[🔍] Đang tìm kiếm thông tin trong catalog...")

    response = rag_generate_answer(vectorstore, question)
    print("\n[🤖] Trợ lý trả lời:")
    print(response)
