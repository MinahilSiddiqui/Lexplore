# rag_engine.py

import os
import fitz  # PyMuPDF
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# Store chunks & embeddings
doc_chunks = []
doc_embeddings = []
index = None

# Split long text into chunks
def split_text(text, chunk_size=500):
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Load and split PDF
def load_pdf(uploaded_file):
    global doc_chunks, doc_embeddings, index
    doc_chunks = []

    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in doc:
        text = page.get_text().strip()
        if text:
            for chunk in split_text(text):
                doc_chunks.append(chunk)

    doc_embeddings = EMBEDDING_MODEL.encode(doc_chunks)
    index = faiss.IndexFlatL2(doc_embeddings.shape[1])
    index.add(np.array(doc_embeddings))

# Query the document
def query_doc(question, top_k=3):
    question_embedding = EMBEDDING_MODEL.encode([question])
    D, I = index.search(np.array(question_embedding), top_k)
    top_chunks = [doc_chunks[i] for i in I[0]]
    return "\n\n".join(top_chunks)