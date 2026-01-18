# 🚀 **Retrievers in LangChain**

Retrievers are one of the most important building blocks in any **RAG (Retrieval-Augmented Generation)** system.
Think of a retriever as the *search engine* inside your AI assistant.

```
LLM = The brain (thinks and generates answers)
Retriever = The search system (finds relevant information)
Vector Store = The long-term memory (stores all knowledge)
```

---

# 1️⃣ **What Is a Retriever?**

A **Retriever** is a LangChain component that:

* Accepts a **user query**
* Searches a **data source** (Wikipedia, PDF files, vector DB, APIs, etc.)
* Returns the **most relevant documents** as a list of `Document` objects
* Works as a **Runnable** (can be inserted in chains)

### ⚡ Why we need Retrievers?

LLMs alone **hallucinate** when they don’t know facts.
Retrievers supply **ground-truth context** → LLM uses that to answer correctly.

### 📌 Output of a Retriever:

A list like:

```python
[
  Document(page_content="...", metadata={...}),
  Document(page_content="...", metadata={...})
]
```

---

# 2️⃣ **Where Retrievers Fit in RAG Architecture**

```
User Question
      ↓
Retriever (search)
      ↓
Relevant Documents
      ↓
LLM (answer using retrieved context)
      ↓
Response
```

Retrievers sit **before** the LLM inside the pipeline.

---

# 3️⃣ **Retriever Category Breakdown**

Retrievers can be grouped in two ways:

| Category                     | Meaning                          | Examples                                    |
| ---------------------------- | -------------------------------- | ------------------------------------------- |
| **Based on Data Source**     | From where documents are fetched | Wikipedia, Vector DB, File-based retrievers |
| **Based on Search Strategy** | How documents are selected       | MMR, Multi-Query, Contextual Compression    |

Both can be combined.
Example → You can have a vector retriever + MMR.

---

# 4️⃣ **Core Types of Retrievers**

Below is the complete explanation of the retrievers you will actually use in real RAG systems.

---

---

# ⭐ 4.1 Wikipedia Retriever

### 🔎 What it does?

* Queries Wikipedia API directly.
* Uses **keyword search** (bag-of-words).
* Good for general knowledge or testing a RAG pipeline quickly.

### 📌 When to use?

* Early prototyping
* Open-domain RAG systems

### Example Code

```python
from langchain_community.retrievers import WikipediaRetriever

retriever = WikipediaRetriever(
    top_k_results=3,
    lang="en"
)

docs = retriever.invoke("What is diabetes?")
for d in docs:
    print(d.page_content[:300])
```

---

---

# ⭐ 4.2 Vector Store Retriever (Most Common)

### 🧠 Purpose?

Perform **semantic search** on your documents.

### Flow:

1. Convert all documents → embeddings → store them in vector DB.
2. Convert user query → embedding.
3. Retrieve top-k closest vectors.

### Benefits:

* Semantic understanding
* Scales with document size
* Foundation of every production RAG system

### Example with Chroma

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

docs = [
    Document(page_content="Root canal is a dental procedure."),
    Document(page_content="Cardiology deals with heart issues.")
]

vector_store = Chroma.from_documents(
    docs,
    embedding=OpenAIEmbeddings()
)

retriever = vector_store.as_retriever(search_kwargs={"k": 2})

results = retriever.invoke("What is dental procedure?")
print(results)
```

---

---

# ⭐ 4.3 MMR Retriever (Maximum Marginal Relevance)

### Problem it solves:

Normal similarity search returns **similar but redundant** documents.

MMR balances:

* Relevance
* Diversity (removes duplicates)

### How it works:

* Select the most relevant document.
* Next pick documents that are relevant *but not similar to already selected*.

### Formula:

```
score = λ * similarity_with_query - (1-λ) * similarity_with_selected_docs
```

### When to use?

* Long documents with repeated sections
* Need diverse perspectives
* Complex Q&A systems

### Example Code

```python
retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "lambda_mult": 0.5}
)

docs = retriever.invoke("Explain root canal")
```

---

---

# ⭐ 4.4 Multi-Query Retriever (Handles Ambiguous Queries)

### Purpose:

When user queries are broad or vague like:

* “Tell me about diabetes”
* “Explain treatment options”

LLM generates **multiple variations** of the query.

### Example:

Original query: “How to treat diabetes?”
Generated queries:

* “medications for diabetes”
* “diet plan for diabetes”
* “insulin use guidelines”
* “lifestyle changes for diabetes”

Each query → retriever → combined results.

### Benefit:

* Better coverage
* Reduced ambiguity
* High-quality retrieval

### Code Example

```python
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

multi_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=llm
)

docs = multi_retriever.invoke("Tell me about diabetes treatment")
```

---

---

# ⭐ 4.5 Contextual Compression Retriever (Advanced + Production Ready)

### Problem it solves:

Vector search retrieves **full documents**, but only small parts are relevant.

LLM may get:

* Irrelevant noise
* Mixed topics
* Long context → high cost

### Solution:

1. Retrieve documents normally
2. Send them to a **compressor** (LLM)
3. Extract only relevant text
4. Return smaller, high-quality context

### Example:

A 2-page PDF → becomes 3–4 lines of relevant text.

### Code Example

```python
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(ChatOpenAI(model="gpt-4o-mini"))

compression_retriever = ContextualCompressionRetriever(
    base_retriever=retriever,
    compressor=compressor
)

docs = compression_retriever.invoke("What is root canal?")
```

---

# 5️⃣ Additional Advanced Retrievers (Short Notes)

| Retriever                          | Purpose                                               |
| ---------------------------------- | ----------------------------------------------------- |
| **Parent Document Retriever**      | Retrieve small chunks but return full parent document |
| **Time-Weighted Vector Retriever** | Useful for chat history, prioritizes recent messages  |
| **Self-Query Retriever**           | LLM queries metadata fields (e.g., date, author)      |
| **Multi-Retriever**                | Combine several retrievers and merge results          |
| **Ensemble Retriever**             | Weighted combination of search strategies             |

---

# 6️⃣ How to Choose the Right Retriever (Practical Guide)

### If your dataset is *private PDFs / knowledge base*

→ **Vector Store Retriever**
→ Add **MMR** if redundancy is high
→ Add **Contextual Compression** if documents are long

### If user queries are vague

→ **Multi-Query Retriever**

### If your system uses metadata (tags, categories)

→ **Self-Query Retriever**

### If you need open-domain research

→ **Wikipedia Retriever**

---

# 7️⃣ Production Best Practices (Very Important)

### ✔ Use embeddings model suitable to domain

* Healthcare → `bge-large` or `OpenAI text-embedding-3-large`

### ✔ Chunk your documents correctly

* 300–500 tokens
* With overlaps (50–100 tokens)

### ✔ Avoid using raw retriever without rerank

* Always use Rerank or Compression for accuracy

### ✔ Cache your retriever outputs

* Saves cost
* Faster responses

### ✔ Log retrieval context

* For debugging
* For evaluation (RAGAS)

---

# 8️⃣ End-to-End Template (Professional Sample Code)

This is a minimal but production-quality RAG retriever pipeline.

```python
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.doc_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# 1. Load documents
loader = TextLoader("healthcare_knowledge.txt")
docs = loader.load()

# 2. Chunking
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=80)
docs = splitter.split_documents(docs)

# 3. Create vector store
vector_store = Chroma.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings()
)

# 4. Base retriever (semantic)
base_retriever = vector_store.as_retriever(search_kwargs={"k": 4})

# 5. Add compression layer
compressor = LLMChainExtractor.from_llm(ChatOpenAI(model="gpt-4o-mini"))
retriever = ContextualCompressionRetriever(
    base_retriever=base_retriever,
    compressor=compressor
)

# 6. Use retriever in RAG pipeline
query = "Explain symptoms of acute pancreatitis"
results = retriever.invoke(query)

for d in results:
    print(d.page_content)
```

---

# 🎯 Final Summary (Short + Clear)

* Retrievers fetch relevant documents for LLMs.
* They are essential for building reliable RAG systems.
* Two categories:
  **Data Source based** (Wikipedia, Vector DB)
  **Search Strategy based** (MMR, Multi-query, Compression)
* Most useful in production:
  **Vector Retriever + Compression + MMR**
* Use Multi-Query for ambiguous user prompts.
* Compress long documents before passing to LLM.
