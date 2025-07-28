from transformers import pipeline
import os

# Thêm token Hugging Face
HUGGINGFACE_TOKEN = os.getenv("HF_TOKEN")  # hoặc hardcode trực tiếp nếu bạn đang test

# Tạo pipeline từ mô hình open-instruct
llm_pipeline = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    tokenizer="google/flan-t5-base",
    token=HUGGINGFACE_TOKEN,  # Nếu dùng token cá nhân để load từ HuggingFace
    max_new_tokens=128,
    do_sample=True,
    temperature=0.7,
)

def call_llm(prompt: str) -> str:
    output = llm_pipeline(prompt)
    return output[0]["generated_text"]
