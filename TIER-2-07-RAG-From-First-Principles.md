# TIER 2-07: RAG From First Principles
## Retrieval-Augmented Generation

---

## The Problem RAG Solves

### Without RAG
```
User: "What's our company's return policy?"

LLM thinks: "I was trained in 2023. I don't have company-specific info."
LLM responds: "I don't know your specific policy."

Result: ❌ Useless
```

### With RAG
```
User: "What's our company's return policy?"

System steps:
1. Search company docs: "Returns must occur within 30 days"
2. Give context to LLM: "Here's our policy..."
3. LLM responds: "Returns must occur within 30 days..."

Result: ✅ Accurate, current, specific
```

---

## RAG Architecture

```
User Query
    ↓
1. RETRIEVE: Search for relevant documents
    ↓
2. Combine: Query + Retrieved Documents
    ↓
3. AUGMENT: Give context to LLM
    ↓
4. GENERATE: LLM produces answer using context
    ↓
Answer
```

---

## Step-by-Step RAG Process

### Step 1: Load Documents
```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("company_handbook.pdf")
documents = loader.load()
# Result: List of Document objects with content
```

### Step 2: Split Into Chunks
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = splitter.split_documents(documents)
# Result: ~100 smaller documents (chunks)
```

### Step 3: Create Embeddings
```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
# Result: Ready to embed text
```

### Step 4: Store in Vector Database
```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory="./db"
)
# Result: Searchable vector database
```

### Step 5: Create Retriever
```python
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}  # Return top 5 chunks
)
# Result: Can retrieve relevant documents
```

### Step 6: Create RAG Chain
```python
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4"),
    chain_type="stuff",
    retriever=retriever
)
# Result: Full RAG pipeline
```

### Step 7: Ask Questions
```python
answer = qa.invoke("What's the return policy?")
print(answer)
# Result: Accurate answer based on documents
```

---

## What Happens Inside the RAG Chain

### The "stuff" Method
```
1. User question: "What is policy X?"
2. Retrieve top 5 chunks from database
3. Combine all chunks + question into single prompt:
   
   "Context from documents:
    [Chunk 1]
    [Chunk 2]
    [Chunk 3]
    [Chunk 4]
    [Chunk 5]
    
    Question: What is policy X?
    Answer:"
    
4. Send to LLM with all context
5. LLM generates answer based on context

Result: Answer grounded in your documents
```

---

## Advanced: Different RAG Methods

### Method 1: stuff
Works with small documents
```python
qa = RetrievalQA.from_chain_type(
    chain_type="stuff",  # Just concatenate
    retriever=retriever,
    llm=llm
)
```

### Method 2: map_reduce
For large documents:
```python
qa = RetrievalQA.from_chain_type(
    chain_type="map_reduce",  # Summarize each doc, then combine
    retriever=retriever,
    llm=llm
)
```

### Method 3: refine
Iterative improvement:
```python
qa = RetrievalQA.from_chain_type(
    chain_type="refine",  # Build answer incrementally
    retriever=retriever,
    llm=llm
)
```

---

## Real Example: Company Knowledge Base

```python
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# 1. Load all PDFs from a directory
loader = DirectoryLoader("./company_docs", glob="**/*.pdf")
documents = loader.load()

# 2. Split
splitter = RecursiveCharacterTextSplitter(chunk_size=500)
chunks = splitter.split_documents(documents)

# 3. Embed and store
vectorstore = Chroma.from_documents(
    chunks,
    OpenAIEmbeddings(),
    persist_directory="./company_knowledge"
)

# 4. Create RAG
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4"),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# 5. Use it!
questions = [
    "What's our vacation policy?",
    "How do I submit an expense report?",
    "What are our office hours?"
]

for q in questions:
    answer = qa.invoke(q)
    print(f"Q: {q}")
    print(f"A: {answer}")
    print()
```

---

## Improving RAG Quality

### Problem 1: Irrelevant Context
```
Question: "Return policy?"
Retrieved: [Info about shipping, unrelated FAQ, ...]
Result: ❌ LLM confused by irrelevant context
```

**Solution: Better retrieval**
```python
# Increase k (get more results, let LLM filter)
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 10}  # More results
)

# Use filters
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5,
        "filter": {"source": "policies.pdf"}
    }
)
```

### Problem 2: Lost Information
```
Question: "What happened in section 3?"
Retrieved: Sections 2, 4, 5 (missed 3!)
Result: ❌ Missing key information
```

**Solution: Better chunking**
```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Larger chunks
    chunk_overlap=200     # More overlap
)
```

### Problem 3: Token Limit Exceeded
```
Question + 10 chunks + system prompt = 12,000 tokens
Context window: 4,096 tokens
Result: ❌ Error
```

**Solution: Use map_reduce or refine**
```python
qa = RetrievalQA.from_chain_type(
    chain_type="map_reduce",  # Summarize each doc first
    retriever=retriever,
    llm=llm
)
```

---

## Monitoring RAG Quality

### Check Retrieved Documents
```python
# See what documents were retrieved
docs = retriever.get_relevant_documents("query")

for doc in docs:
    print(f"Source: {doc.metadata.get('source')}")
    print(f"Content: {doc.page_content[:200]}...")
    print()
```

### Check Relevance Scores
```python
# See similarity scores
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 10}
)

# Get with scores
docs_with_scores = vectorstore.similarity_search_with_scores(
    "query", k=10
)

for doc, score in docs_with_scores:
    print(f"Relevance: {score:.2f} - {doc.page_content[:50]}...")
    
    # Flag low-scoring results
    if score < 0.6:
        print("  ⚠️ Low relevance!")
```

---

## Production Checklist

### Before Deploying RAG

- [ ] **Document Quality** - Are documents accurate and up-to-date?
- [ ] **Chunking Strategy** - Is chunk size appropriate?
- [ ] **Vector Quality** - Are embeddings good?
- [ ] **Retrieval Testing** - Does it find relevant docs?
- [ ] **Performance** - Is it fast enough?
- [ ] **Hallucination Check** - Does it stay grounded in docs?
- [ ] **Monitoring** - Can you track quality?
- [ ] **Fallback** - What if retrieval fails?

---

## Real Code: End-to-End RAG Application

```python
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

class CompanyRAG:
    def __init__(self, docs_path="./docs", db_path="./db"):
        self.docs_path = docs_path
        self.db_path = db_path
        self.qa = None
        
    def load_documents(self):
        """Load all PDFs from directory"""
        documents = []
        for pdf_file in Path(self.docs_path).glob("*.pdf"):
            loader = PyPDFLoader(pdf_file)
            documents.extend(loader.load())
        return documents
    
    def setup(self):
        """Initialize RAG pipeline"""
        # Load
        documents = self.load_documents()
        
        # Split
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        chunks = splitter.split_documents(documents)
        
        # Embed and store
        vectorstore = Chroma.from_documents(
            chunks,
            OpenAIEmbeddings(),
            persist_directory=self.db_path
        )
        
        # Create QA chain
        self.qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model="gpt-4"),
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )
    
    def query(self, question):
        """Ask a question"""
        if not self.qa:
            self.setup()
        return self.qa.invoke(question)

# Use it
rag = CompanyRAG()
answer = rag.query("What is the return policy?")
print(answer)
```

---

## Self-Check

Can you answer:

- [ ] "What does RAG stand for?" (Retrieval-Augmented Generation)
- [ ] "Why is RAG useful?" (Gives LLMs access to current, specific documents)
- [ ] "What are the 4 steps in RAG?" (Load, Split, Embed, Retrieve, Generate)
- [ ] "What's the 'stuff' method?" (Concatenate all chunks + question into one prompt)
- [ ] "How do you improve RAG quality?" (Better chunking, filtering, monitoring)

Ready for **[TIER-2-08-Building-Your-First-RAG-App.md](TIER-2-08-Building-Your-First-RAG-App.md)** →

Next: Build a working RAG application from scratch.
