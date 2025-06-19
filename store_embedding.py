from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from extract import extract_sections_from_pdf
from tqdm import tqdm

# === Step 1: Extract PDF Sections ===
pdf_path = "E:/legal/panelcode.pdf"
sections = extract_sections_from_pdf(pdf_path)

# === Step 2: Setup LangChain Embeddings ===
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# === Step 3: Setup Text Splitter ===
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# === Step 4: Prepare Data ===
texts = []
metadatas = []

for sec in tqdm(sections, desc="Processing sections"):
    section_id = str(sec["section"]).strip().lower()
    chunks = text_splitter.split_text(sec["text"])

    for i, chunk in enumerate(chunks):
        texts.append(chunk)
        metadatas.append({
            "section": section_id,
            "chunk": i
        })

# === Step 5: Store using LangChain's Chroma ===
vectordb = Chroma.from_texts(
    texts=texts,
    embedding=embedding_model,
    metadatas=metadatas,
    persist_directory="chroma_db"  # ✅ same directory used by query
)
vectordb.persist()

print(f"✅ Stored {len(texts)} chunks using LangChain Chroma.")
