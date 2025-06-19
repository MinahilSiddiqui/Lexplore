import os
import re
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
import os

os.environ["OPENROUTER_API_KEY"] = "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"

# === Load Environment ===
load_dotenv()
#os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# === Load Vector Store and Embedding Model ===
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectordb = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding_model
)

# === Setup Language Model ===
llm = ChatOpenAI(
    model_name="mistralai/mistral-7b-instruct",
    temperature=0.3,
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1"
)



def query_law(question: str) -> dict:
    normalized_question = question.strip().lower()

    # === STEP 1: Extract Section ===
    match = re.search(r'(section|sec\.?)\s*(\d{1,4}[a-zA-Z\-]*)', normalized_question)
    section = match.group(2).strip().lower() if match else None

    print(f"[DEBUG] Parsed section ID: {section if section else 'None (semantic fallback)'}")

    retrieved_docs = []

    try:
        if section:
            # === STEP 2A: Try Filtered Section Match ===
            section_retriever = vectordb.as_retriever(
                search_kwargs={"k": 5},
                filter_fn=lambda metadata: section in metadata.get("section", "").lower()
            )
            retrieved_docs = section_retriever.invoke(normalized_question)

            print(f"[DEBUG] Retrieved {len(retrieved_docs)} docs by section match")

        if not retrieved_docs:
            # === STEP 2B: Fallback to Semantic Search ===
            fallback_retriever = vectordb.as_retriever(search_kwargs={"k": 5})
            retrieved_docs = fallback_retriever.invoke(normalized_question)
            print(f"[DEBUG] Retrieved {len(retrieved_docs)} docs using semantic fallback")

    except Exception as e:
        print(f"❌ Retrieval failed: {e}")
        return {"result": f"Retrieval error: {e}", "source_documents": []}

    # === STEP 3: Show Retrieved Content ===
    print("\n==== Retrieved Documents ====")
    for i, doc in enumerate(retrieved_docs):
        print(f"Doc {i+1} - Section: {doc.metadata.get('section', 'N/A')}")
        print(doc.page_content[:200])
        print("-" * 30)

    # === STEP 4: Build Prompt for LLM ===
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    final_prompt = (
        "You are a legal expert trained only on the Pakistan Penal Code.\n"
        "Only use the law sections below to answer the user's question.\n"
        "If no relevant law is found, say: 'No relevant section found in Pakistan Penal Code.'\n\n"
        f"---\nLAW EXTRACTS:\n{context if context else 'None'}\n---\n\n"
        f"Question: {normalized_question}\n"
        "Answer:"
    )

    try:
        response = llm.invoke(final_prompt)
        return {
            "result": response.content.strip(),
            "source_documents": retrieved_docs
        }
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        return {"result": f"LLM Error: {e}", "source_documents": []}
