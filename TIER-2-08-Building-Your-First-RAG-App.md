# TIER 2-08: Building Your First RAG App
## From Zero to Working Application

---

## Project: Document Q&A System

We'll build a complete RAG app that lets you ask questions about any PDF document.

---

## Step 1: Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install langchain langchain-openai langchain-community chromadb pypdf
```

---

## Step 2: File Structure

```
project/
├── main.py           # Main app
├── config.py         # Configuration
├── .env              # API keys (don't commit!)
├── data/
│   └── documents/    # PDF files go here
└── db/               # Vector database (created by app)
```

---

## Step 3: Configuration (.env)

Create `.env` file:
```
OPENAI_API_KEY=sk-...
```

Load it in Python:
```python
# config.py
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_PATH = "./db"
DATA_PATH = "./data/documents"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
```

---

## Step 4: Document Loader

```python
# loader.py
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from config import DATA_PATH

class DocumentLoader:
    def __init__(self, data_path=DATA_PATH):
        self.data_path = Path(data_path)
    
    def load_documents(self):
        """Load all PDFs from directory"""
        documents = []
        pdf_files = list(self.data_path.glob("*.pdf"))
        
        if not pdf_files:
            raise FileNotFoundError(f"No PDFs found in {self.data_path}")
        
        print(f"Found {len(pdf_files)} PDF files")
        
        for pdf_file in pdf_files:
            print(f"Loading: {pdf_file.name}")
            loader = PyPDFLoader(str(pdf_file))
            docs = loader.load()
            documents.extend(docs)
        
        print(f"Total pages loaded: {len(documents)}")
        return documents
```

---

## Step 5: Vector Store Manager

```python
# vector_store.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from config import DB_PATH, CHUNK_SIZE, CHUNK_OVERLAP

class VectorStoreManager:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
    
    def create_from_documents(self, documents):
        """Create vector store from documents"""
        print("Splitting documents into chunks...")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks")
        
        print("Creating embeddings and storing...")
        self.vectorstore = Chroma.from_documents(
            chunks,
            self.embeddings,
            persist_directory=self.db_path
        )
        print(f"Vector store created at {self.db_path}")
    
    def load_existing(self):
        """Load existing vector store"""
        print("Loading existing vector store...")
        self.vectorstore = Chroma(
            persist_directory=self.db_path,
            embedding_function=self.embeddings
        )
        return self.vectorstore
    
    def get_retriever(self, k=5):
        """Get retriever for RAG"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        
        return self.vectorstore.as_retriever(
            search_kwargs={"k": k}
        )
```

---

## Step 6: RAG Chain

```python
# rag_chain.py
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class RAGChain:
    def __init__(self, retriever):
        self.retriever = retriever
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.7)
        
        # Custom prompt
        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""Use the following context to answer the question.
If the context doesn't contain information to answer, say "I don't have that information in the documents."

Context:
{context}

Question: {question}

Answer:"""
        )
    
    def create_qa_chain(self):
        """Create QA chain"""
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=True
        )
        return self.qa_chain
    
    def query(self, question):
        """Ask a question"""
        result = self.qa_chain({"query": question})
        return result
```

---

## Step 7: Main Application

```python
# main.py
from loader import DocumentLoader
from vector_store import VectorStoreManager
from rag_chain import RAGChain
from config import DB_PATH
from pathlib import Path

def main():
    print("=== Document Q&A RAG System ===\n")
    
    # Check if vector store exists
    db_exists = Path(DB_PATH).exists()
    
    if db_exists:
        print("Using existing vector store...")
        vs = VectorStoreManager()
        vs.load_existing()
    else:
        print("Creating new vector store...\n")
        
        # Load documents
        loader = DocumentLoader()
        documents = loader.load_documents()
        
        # Create vector store
        vs = VectorStoreManager()
        vs.create_from_documents(documents)
    
    # Create RAG chain
    retriever = vs.get_retriever(k=5)
    rag = RAGChain(retriever)
    qa_chain = rag.create_qa_chain()
    
    # Interactive Q&A
    print("\n=== Ready to Answer Questions ===")
    print("Type 'exit' to quit\n")
    
    while True:
        question = input("Question: ").strip()
        
        if question.lower() == "exit":
            print("Goodbye!")
            break
        
        if not question:
            print("Please enter a question.\n")
            continue
        
        print("\nSearching documents...")
        result = rag.query(question)
        
        print(f"\nAnswer:\n{result['result']}")
        
        # Show sources
        print(f"\n[Sources: {len(result.get('source_documents', []))} documents found]")
        for i, doc in enumerate(result.get('source_documents', []), 1):
            source = doc.metadata.get('source', 'Unknown')
            page = doc.metadata.get('page', 'N/A')
            print(f"  {i}. {source} (Page {page})")
        
        print()

if __name__ == "__main__":
    main()
```

---

## Step 8: Enhanced Version with Web Interface (Optional)

Using Streamlit:

```bash
pip install streamlit
```

```python
# app.py
import streamlit as st
from loader import DocumentLoader
from vector_store import VectorStoreManager
from rag_chain import RAGChain
from pathlib import Path
from config import DB_PATH

st.set_page_config(page_title="Document Q&A", layout="wide")

st.title("📄 Document Question Answering System")

# Sidebar for setup
with st.sidebar:
    st.header("Setup")
    
    if st.button("Initialize Vector Store"):
        with st.spinner("Loading documents..."):
            loader = DocumentLoader()
            documents = loader.load_documents()
            
            vs = VectorStoreManager()
            vs.create_from_documents(documents)
            
            st.success("Vector store created!")

# Main interface
st.header("Ask Your Documents")

question = st.text_input("Enter your question:")

if question:
    with st.spinner("Searching..."):
        vs = VectorStoreManager()
        vs.load_existing()
        retriever = vs.get_retriever(k=5)
        rag = RAGChain(retriever)
        qa_chain = rag.create_qa_chain()
        
        result = rag.query(question)
        
        st.subheader("Answer")
        st.write(result["result"])
        
        st.subheader("Source Documents")
        for i, doc in enumerate(result.get("source_documents", []), 1):
            with st.expander(f"Document {i}"):
                st.write(doc.page_content)
                st.caption(f"Source: {doc.metadata.get('source', 'Unknown')}")
```

Run Streamlit app:
```bash
streamlit run app.py
```

---

## Usage Guide

### First Time Setup

```bash
# 1. Put PDF files in data/documents/
cp your_files/*.pdf data/documents/

# 2. Run the app
python main.py

# 3. Answer questions!
```

### Subsequent Uses

```bash
# App reuses the vector store
python main.py

# It's instant - no reprocessing!
```

---

## Testing Your RAG

### Test 1: Simple Questions
```
Question: "What is the main topic?"
Expected: Answer based on documents
```

### Test 2: Specific Details
```
Question: "What are the specific steps in section 3?"
Expected: Exact information from documents
```

### Test 3: Hallucination Detection
```
Question: "What is something not in the documents?"
Expected: "I don't have that information..."
NOT: Made-up answer
```

---

## Deployment Options

### Option 1: Local (Easiest)
```bash
python main.py
```

### Option 2: Web Server (Streamlit Cloud)
```bash
streamlit run app.py
# Then deploy to Streamlit Cloud
```

### Option 3: API (FastAPI)
```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_question(q: Question):
    result = qa_chain({"query": q.query})
    return {"answer": result["result"]}

# Run: uvicorn app:app --reload
```

---

## Common Issues and Fixes

### Issue 1: "No PDFs found"
```
Fix: Put PDFs in data/documents/ folder
Check: ls data/documents/
```

### Issue 2: "API Key error"
```
Fix: Set OPENAI_API_KEY in .env
Check: echo $OPENAI_API_KEY
```

### Issue 3: "Slow queries"
```
Fix: Reduce chunk_size or k value
Try: CHUNK_SIZE = 1000 (larger chunks, faster)
     k = 3 (fewer documents, faster)
```

### Issue 4: "LLM Hallucinating"
```
Fix: Improve your prompt in RAGChain
Add: "Only use information from the documents"
```

---

## Self-Check

Can you:

- [ ] Set up the project structure?
- [ ] Install dependencies?
- [ ] Load PDF documents?
- [ ] Create and store embeddings?
- [ ] Ask questions and get answers?
- [ ] Deploy the application?

---

## Next Steps

After this project:
- Try with different document types
- Add support for web scraping
- Implement caching for faster queries
- Add user authentication
- Deploy to production

**You've completed TIER 2!** 🎉

---

Ready for **[TIER-3-01-Advanced-RAG-Architectures.md](TIER-3-01-Advanced-RAG-Architectures.md)** →

Next: TIER 3 - Build production-grade systems
