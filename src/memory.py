import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


def init_memory(texts):
    if not texts:
        raise ValueError("No texts provided to initialize FAISS memory.")

    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.from_texts(texts=texts, embedding=embedding_model)


def add_to_memory(memory, new_texts):
    for t in new_texts:
        memory.add_texts([t])
