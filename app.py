import streamlit as st
import requests
from PIL import Image
import os


# --- Config ---
YOLO_API_URL = "http://localhost:8000/detect"
DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"
DIFY_API_KEY = os.getenv("DIFY_API_KEY")


st.title("🔍 YOLO Detection via FastAPI")

# Upload image
uploaded_image = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    st.image(uploaded_image, caption="🖼️ Uploaded Image", use_column_width=True)

    if st.button("🚀 Run Detection"):
        with st.spinner("Sending image to YOLO API..."):
            files = {
                'image': (uploaded_image.name, uploaded_image.getvalue(), uploaded_image.type)
            }

            try:
                response = requests.post(
                    "http://localhost:8000/detect",
                    files=files,
                    headers={"accept": "application/json"}
                )
                response.raise_for_status()
                result = response.json()

                # ✅ Lấy danh sách nhãn và hiển thị theo dạng text
                labels = result.get("labels", [])
                if labels:
                    st.subheader("🔎 Detection Result:")
                    for label in labels:
                        st.text(f"Detected label: {label}")
                else:
                    st.warning("⚠️ No labels found.")

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error calling API: {e}")

import streamlit as st
import streamlit.components.v1 as components

st.title("🤖 Chatbot powered by Dify")

# Nhúng iframe
components.html(
    """
    <iframe
        src="https://udify.app/chatbot/fU6vROlbfhKjRvIi"
        style="width: 100%; height: 700px; border: none;"
        allow="microphone">
    </iframe>
    """,
    height=720,  # Chiều cao iframe (hoặc cao hơn tùy bạn)
)
