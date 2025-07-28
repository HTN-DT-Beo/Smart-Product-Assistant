from app.llm.huggingface_llm import call_llm
from langchain.chains import RetrievalQA

def rag_generate_answer(vectorstore, question):
    retriever = vectorstore.as_retriever()

    docs = retriever.get_relevant_documents(question)
    context = "\n\n".join([doc.page_content for doc in docs])

    # Tạo prompt thủ công
    prompt = f"""You are a smart and helpful assistant. The following is product information retrieved from the catalog:

    {context}

    Based on the information above, answer the following question:
    "{question}"
    """

    return call_llm(prompt)
