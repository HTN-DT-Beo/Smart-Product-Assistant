# Smart-Product-Assistant
Smart Product Assistant is an AI system that helps users get instant answers about electronic products by uploading an image and asking a question. It supports sales and customer service for electronic devices.

---
## 🔬 Project Overview
This project is an experimental research-level prototype designed to explore the integration of modern AI tools and APIs. The main goals include:

Getting familiar with Hugging Face APIs

Building image detection APIs using FastAPI

Creating a simple chatbot system using Dify

Integrating the Dify chatbot into a web-based frontend

The dataset used in this project consists of product images and related metadata collected from various e-commerce platforms. After collection, the data was augmented and annotated using Roboflow to support object detection and retrieval-based chatbot interactions.

---
## 📝 Project Summary

### 📌 Components Implemented
#### Console
- **Detection:** YOLOv8  
- **RAG:** sentence-transformers + FAISS
- **LLM:** google/flan-t5-base 

#### Apply Dify
- **Detection:** YOLOv8  
- **Chatbot:** Dify (GPT-4)

---
### ⚙️ Technologies Used
#### 🧠 AI & NLP
Hugging Face Transformers
→ Utilized the sentence-transformers/all-MiniLM-L6-v2 model to generate vector embeddings for text, which are used in the Retrieval-Augmented Generation (RAG) component.

Dify.AI
→ A low-code/no-code platform for building chatbots with built-in LLM integration and support for RAG pipelines through a visual interface.

#### 🖼️ Computer Vision
YOLO (You Only Look Once)
→ An object detection model used to identify products in images. It is deployed as a standalone API using FastAPI.

Roboflow
→ Used for image annotation and preprocessing, including tasks like augmentation, resizing, and exporting to YOLO-compatible formats.

#### 🧩 Backend APIs
FastAPI
→ A modern Python web framework used to build RESTful APIs for:

Receiving images and running object detection via YOLO

Returning detection results in JSON format

#### 🌐 Frontend Integration
Streamlit
→ A simple Python-based web UI framework used to:

Upload images and send them to the YOLO API

Display object detection results (labels)

Embed the Dify chatbot using an <iframe>

#### 📚 Vector Database (RAG)
FAISS (Facebook AI Similarity Search)
→ Used to store and query vector embeddings of product descriptions for efficient semantic search.

LangChain
→ Utilized to build the RAG pipeline:
* Load data from a CSV file

* Split text into manageable chunks

* Generate embeddings

* Perform retrieval to support chatbot responses
---

### ✅ Results

- 📷 **Image Output**  
![Detect Console](https://github.com/HTN-DT-Beo/Smart-Product-Assistant/blob/main/demo/detect_console.png)
![Chatbot Console](https://github.com/HTN-DT-Beo/Smart-Product-Assistant/blob/main/demo/chatbot_console.png)
![Detect Streamlit](https://github.com/HTN-DT-Beo/Smart-Product-Assistant/blob/main/demo/detect.png)
![Chatbot Streamlit](https://github.com/HTN-DT-Beo/Smart-Product-Assistant/blob/main/demo/chatbot.png)
