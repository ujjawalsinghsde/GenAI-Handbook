# Vector Stores in LangChain

## Why Vector Stores Are Essential for RAG

Building effective Retrieval-Augmented Generation and semantic search systems requires the ability to:

* Convert text into numerical embeddings
* Store and index these embeddings efficiently
* Perform similarity searches based on vector distance
* Manage associated metadata
* Enable fast approximate nearest-neighbor queries

---

## 2. **What Exactly Is a Vector Store?**

A **vector store** is a system that:

* 🧠 **Stores embeddings** (high-dim vectors)
* 📄 Stores **documents + metadata**
* 🔍 Performs **similarity searches**
* ⚙️ Supports **CRUD operations**
* 🚀 Uses **indexing** for fast retrieval

Think of it like a special database where:

> **Instead of searching text, you search for closest vectors.**

---

## 3. **Vector Store vs Vector Database (Clear Difference)**

| Feature  | Vector Store                      | Vector Database                             |
| -------- | --------------------------------- | ------------------------------------------- |
| Purpose  | Store vectors + similarity search | Production-grade DB with scaling & security |
| Scale    | Small–medium apps                 | Large & distributed                         |
| Features | CRUD, indexing                    | Backup, replication, ACID, auth             |
| Examples | FAISS, Chroma                     | Pinecone, Milvus, Weaviate                  |
| Relation | Simple library                    | Full database                               |

**Every vector DB is a vector store, but not every vector store is a vector database.**

---

## 4. **Core Concepts You MUST Know**

### 4.1 Embeddings

Text → Embedding (array of floating numbers).
Example:
`[0.12, -0.44, 0.88, ...]` (768–4096 dimensions depending on model)

### 4.2 Similarity Metrics

Used to compare vectors:

* **Cosine Similarity (most common)**
* Euclidean Distance
* Dot Product

### 4.3 Indexing (for speed)

Without indexing:
→ linear scan → slow for millions of vectors.

With indexing (e.g., HNSW, IVF):
→ Fast Approximate Nearest Neighbor search
→ 100x–1000x faster.

---

## 5. **How LangChain Uses Vector Stores (Important for RAG Architecture)**

LangChain provides:

* A **unified interface** for all vector stores.
* Ability to **swap Chroma → Pinecone → FAISS** with minimal code changes.
* Built-in retrievers for querying vectors.

### Popular LangChain-supported stores:

* Chroma
* Pinecone
* FAISS
* Qdrant
* Weaviate
* Milvus

---

## 6. **Internal Data Model (How Chroma Organizes Data)**

Chroma’s hierarchy:

```
Tenant → Database → Collection → Documents → (Embedding + Metadata)
```

Each document contains:

* `content` (text)
* `embedding`
* `metadata`
* `id`

---

## 7. **RAG Flow With Vector Store (High-Level Architecture)**

```
User Query  
     ↓  
LLM → Query Embedding  
     ↓  
Vector Store (similarity search)  
     ↓  
Top-K Relevant Documents  
     ↓  
LLM → Final Answer
```

---

# 🧪 **8. Practical Guide: Chroma + LangChain (Clean & Professional Code)**

Below is **professional-quality** Python code suitable for production-style notes.

> ✔️ MIT clean
> ✔️ Structured
> ✔️ Includes CRUD, similarity search, metadata filters

---

## **8.1 Installation**

```python
!pip install langchain langchain-openai chromadb tiktoken
```

---

## **8.2 Setup Environment**

```python
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
```

---

## **8.3 Create Documents**

```python
docs = [
    Document(
        page_content="Virat Kohli plays for RCB in IPL and is one of the best batsmen.",
        metadata={"player": "Kohli", "team": "RCB"}
    ),
    Document(
        page_content="Rohit Sharma is the captain of Mumbai Indians and an explosive opener.",
        metadata={"player": "Rohit", "team": "MI"}
    ),
    Document(
        page_content="MS Dhoni is the captain of CSK and known for his calm leadership.",
        metadata={"player": "Dhoni", "team": "CSK"}
    )
]
```

---

## **8.4 Create Vector Store**

```python
embeddings = OpenAIEmbeddings()

vector_store = Chroma(
    collection_name="ipl_players",
    embedding_function=embeddings,
    persist_directory="./chroma_store"
)

vector_store.add_documents(docs)
vector_store.persist()
```

---

## **8.5 Similarity Search**

```python
query = "Which player is a calm leader?"
results = vector_store.similarity_search(query, k=2)

for r in results:
    print(r.page_content, r.metadata)
```

---

## **8.6 Similarity Search with Scores**

```python
results = vector_store.similarity_search_with_score("Mumbai Indians captain", k=2)

for doc, score in results:
    print(score, doc.page_content)
```

---

## **8.7 Metadata Filter**

```python
results = vector_store.similarity_search(
    "captain", 
    k=2,
    filter={"team": "CSK"}
)

for r in results:
    print(r.page_content)
```

---

## **8.8 Update Document (by ID)**

```python
doc_ids = vector_store.get()['ids']

vector_store.update_document(
    doc_ids[0],
    Document(
        page_content="Updated: Virat is a legendary batsman for RCB.",
        metadata={"updated": True}
    )
)
```

---

## **8.9 Delete Document**

```python
vector_store.delete([doc_ids[1]])
```

---

# 9. **Advanced Topics (Production-Level Knowledge)**

## 9.1 Index Types

Different vector DBs support:

* **HNSW** (Weaviate, Qdrant)
* **IVF / Flat** (FAISS)
* **DiskANN** (Microsoft)
* **ScaNN** (Google)

Choose based on:

* dataset size (50k vs 50M)
* latency requirements
* accuracy needed

---

## 9.2 Retrieval Techniques

In LangChain you can use:

### 1. **Similarity Search**

Find **top-K closest vectors**.

### 2. **Max Marginal Relevance (MMR)**

Improves diversity in retrieved results.

```python
vector_store.max_marginal_relevance_search(query, k=3)
```

### 3. **Hybrid Search (Embedding + Keyword)**

Some DBs support hybrid retrieval (e.g., Weaviate, Pinecone).

---

## 9.3 Choosing the Right Vector DB

| Dataset Size     | Recommended       |
| ---------------- | ----------------- |
| < 50k            | Chroma / FAISS    |
| 50k – 1M         | Qdrant / Weaviate |
| > 1M, production | Pinecone / Milvus |
| On-device apps   | FAISS / Chroma    |

---

# 10. **Best Practices for RAG Vector Stores**

* Always normalize text (lowercase, clean HTML).
* Use chunking (300–1000 tokens per chunk).
* Add rich metadata (source, title, tags).
* Persist vector store for faster loads.
* Use embeddings suitable for your tasks:

  * Text: **OpenAI text-embedding-3-large**
  * Code: **OpenAI code embedding**
* Cache results whenever possible.

---

# 11. **Final Summary (Easy to Remember)**

* **Vector stores** are essential for semantic search and RAG.
* Embeddings enable comparison of meaning, not keywords.
* LangChain provides a unified interface for many vector stores.
* Chroma is lightweight and perfect for local setups.
* For production-scale, choose Pinecone, Milvus, Weaviate, or Qdrant.
* Use metadata, indexing, and chunking to optimize retrieval.

