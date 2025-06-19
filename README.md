### README for **Lexplore**

---

## **Lexplore: Legal Exploration Assistant**

**Lexplore** is an intelligent, multimodal conversational assistant designed to assist users with legal information, document analysis, and web-based research. Powered by large language models (LLMs), the app integrates natural language processing, voice input/output, and translation capabilities for a seamless user experience.

---

### **Features**

1. **Multimodal Interaction**:

   * **Voice Input**: Query using spoken language.
   * **Text Input**: Ask questions via a chat interface.
2. **PDF Analysis**:

   * Upload legal documents and ask context-specific questions.
3. **Web Search Integration**:

   * Retrieve and summarize search results from the web.
4. **Query Classification**:

   * Dynamically routes queries to the appropriate module (General, PDF, Web Search, or Legal).
5. **Translation and Text-to-Speech**:

   * Provides responses in English or Urdu.
   * Converts responses to audio for voice feedback.

---

### **Tech Stack**

* **Frontend**: Streamlit for interactive UI.
* **Backend**: Python for routing and processing.
* **APIs and Utilities**:

  * `llm_api`: Handles queries sent to the language model.
  * `web_search`: Integrates web search capabilities.
  * `rag_engine`: Enables retrieval-augmented generation (RAG) for document-based QA.
  * `query_law`: Processes and retrieves legal information.
  * `tts_utils`: Text-to-speech conversion.
  * `translation_utils`: Translation between English and Urdu.

---

### **Setup and Installation**

#### **Prerequisites**

* Python 3.8 or later.
* A `.env` file containing API keys for required services.

#### **Installation**

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/lexplore.git
   cd lexplore
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Set up the `.env` file:

   ```plaintext
   OPENAI_API_KEY=your_openai_api_key
   OTHER_API_KEYS=...
   ```

#### **Run the App**

```bash
streamlit run app.py
```

---

### **Usage**

1. **Upload a PDF**: Use the sidebar to upload a legal document.
2. **Ask Questions**: Enter queries related to the uploaded document, laws, or general topics.
3. **Switch Modes**: Enable voice input for hands-free operation.
4. **Translation and Audio**: Select the language and use audio feedback as needed.

---

### **Modules**

* **Core Logic**:

  * `classify_query`: Determines the appropriate handling mode for a query.
* **PDF Analysis**:

  * `load_pdf`: Indexes the uploaded document for quick lookups.
  * `query_doc`: Extracts relevant context from the document.
* **Voice Interaction**:

  * `voice_assistant_ui`: Handles real-time voice input and transcription.
* **Web Search**:

  * `search_web`: Retrieves and summarizes web content.

---

### **Future Enhancements**

* Integration with legal databases for more detailed responses.
* Improved natural language understanding for complex queries.
* Support for additional languages and legal systems.

---

### **Contributing**

1. Fork the repository.
2. Create a new feature branch:

   ```bash
   git checkout -b feature-name
   ```
3. Commit and push your changes.
4. Submit a pull request for review.

---

### **License**

This project is licensed under the [MIT License](LICENSE).

---

### **Contact**

For queries or support, contact [Your Name](mailto:your.email@example.com).
