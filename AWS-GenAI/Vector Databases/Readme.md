# 📘 **Vector Databases**

A **vector database** is a special database designed for storing and searching **embeddings** (numerical vectors).
Vectors represent the *meaning* of text, images, audio, or video.
This makes vector DBs essential for **RAG (Retrieval-Augmented Generation)**, semantic search, recommendation systems, and GenAI applications.

Let’s understand everything step-by-step.

---

# 1️⃣ **Introduction to Vector Databases**

A vector database stores **vectors** — high-dimensional number lists that represent the **meaning** of data.

Example vector:

```
[0.12, -0.56, 0.33, 0.88, ...]
```

If two vectors are **close**, their meanings are close.

### 👉 Simple explanation:

**Vector DB = Database that stores meanings of your documents in numerical form and finds the most similar meanings using math.**

Traditional databases store:

* rows
* columns
* tables

Vector DB stores:

* embeddings
* metadata
* meaning-based indexes

---

# 2️⃣ **Use Cases of Vector DBs**

Vector databases are used in all modern AI systems.

### ⭐ 1. RAG (Retrieval-Augmented Generation)

LLM retrieves relevant text chunks from vector DB → gives accurate answers.

### ⭐ 2. Semantic Search

Search by meaning, not keywords:

* “affordable phone” matches “budget smartphone”

### ⭐ 3. Chatbots with company knowledge

Chatbot answers using:

* PDFs
* Word docs
* Internal wiki
* Websites

### ⭐ 4. Recommendations

Used for:

* Product recommendations
* Similar content suggestion

### ⭐ 5. Deduplication / Clustering

Group similar documents with embeddings.

### ⭐ 6. Image search

Search by image similarity.

### ⭐ 7. Fraud detection

Find similar fraudulent patterns.

### ⭐ 8. Personalized content

Match user profile vectors to content vectors.

---

# 3️⃣ **Text Chunking & Embeddings**

Before storing data in a vector database, two steps are required:

---

## ⭐ 3.1 Text Chunking

Large documents are broken into **small pieces (chunks)**.
Why? LLMs retrieve better with short logical chunks.

Example:

* PDF → 100 pages
* Chunked into 300–400 text blocks
* ~200–500 words each

Chunk example:

```
"Refund policy for digital products..."
```

### Best practice:

* Chunk size: 200–500 tokens
* Overlap: 50 tokens

---

## ⭐ 3.2 Embeddings

Embedding = converting text → vector of numbers.

Example:

```
"Apple the fruit" → [0.12, 0.89, ...]
"Apple the company" → [0.95, 0.11, ...]
```

Different meaning → **vector far apart**
Similar meaning → **vectors close**

### Bedrock Embedding Models:

* **Amazon Titan Embeddings v2** (best choice on AWS)
* Llama embeddings
* Mistral embeddings

Embeddings capture meaning → required for semantic search.

---

# 4️⃣ **Vector Similarity Search**

This is the core function of a vector DB.

### 👉 What is similarity search?

It finds the most **similar vectors** to a query vector.

Example query:

> “How can I cancel a digital order?”

Steps:

1. Convert query → embedding
2. Compare embedding with stored vectors
3. Return the **closest matches**

Mathematically, it uses:

* Cosine similarity
* Dot product
* Euclidean distance

### 👉 Why important?

LLM gets the exact relevant chunks → accurate answer.

---

# 5️⃣ **Local Vector DB Setup and CRUD Operations**

You can set up vector DB locally or on cloud.

Common vector DBs:

* **FAISS (local)**
* **Chroma (local)**
* **Milvus**
* **Weaviate**
* **Pinecone**
* **OpenSearch**
* **DynamoDB Vector Search**
* **PostgreSQL + PGVector**

---

## ⭐ 5.1 Setup (Example: Chroma local)

Install:

```bash
pip install chromadb
```

Create DB:

```python
import chromadb

client = chromadb.Client()
collection = client.create_collection("docs")
```

---

## ⭐ 5.2 Insert embeddings (Create)

```python
collection.add(
    ids=["1"],
    documents=["Refund policy for digital goods..."],
    embeddings=[[0.12, 0.88, ...]]
)
```

---

## ⭐ 5.3 Read/Search data (Retrieve)

```python
collection.query(
    query_embeddings=[[0.90, 0.11, ...]],
    n_results=3
)
```

---

## ⭐ 5.4 Update embeddings

```python
collection.update(
    ids=["1"],
    documents=["Updated refund policy..."]
)
```

---

## ⭐ 5.5 Delete embeddings

```python
collection.delete(ids=["1"])
```

---

# 6️⃣ **Querying Vector Embeddings**

Query flow:

```
User Query → Convert to embedding → Similarity Search → Return relevant chunks
```

Example:

```python
embedding = emb_model.embed_query("What is refund policy?")
res = collection.query(query_embeddings=[embedding], n_results=5)
```

Returned chunks feed into:

* Nova
* Claude
* Llama
* Mistral

For generating a final answer.

---

# 7️⃣ **Amazon PGVector & Embeddings**

Amazon Aurora PostgreSQL & RDS PostgreSQL support **pgvector** extension.

### 👉 What is PGVector?

pgvector = Postgres extension that stores vector columns and performs vector search.

### Why it's popular?

* Uses relational DB you already know
* Easy to manage
* Works inside VPC
* No need for extra vector DB service

### Create a vector table:

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id serial PRIMARY KEY,
    content text,
    embedding vector(768)
);
```

### Insert embeddings:

```sql
INSERT INTO documents (content, embedding)
VALUES ('Refund policy text', '[0.12, 0.88, ...]');
```

### Search similar embeddings:

```sql
SELECT content
FROM documents
ORDER BY embedding <-> '[0.90, 0.11, ...]'
LIMIT 5;
```

`<->` is the similarity operator.

### Embeddings:

Use Amazon Titan embedding model:

```python
from langchain_aws import BedrockEmbeddings
emb = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2")
```

---

# 8️⃣ **Deep Dive: Amazon Knowledge Bases for Bedrock**

Knowledge Base = fully managed RAG pipeline.

AWS handles:

### ✔ Document ingestion

✔ Chunking
✔ Embedding generation
✔ Vector storage
✔ Retrieval
✔ RAG-response generation

You only need:

* S3 bucket
* Knowledge Base config
* Bedrock model (Nova/Claude/Llama)

### Running a query:

```python
response = client.retrieve_and_generate(
    knowledgeBaseId="kb-123",
    input={"text": "What is our refund policy?"}
)
```

Then Nova uses:

* Retrieved chunks
* Query
* Your instructions

to produce an accurate answer.

---

# 9️⃣ **Build a Knowledge Base with a Vector Database**

If you want to build manually:

---

## ⭐ Step 1 — Collect documents

Store in S3 or local.

## ⭐ Step 2 — Chunk documents

Split into small blocks.

## ⭐ Step 3 — Generate embeddings

Use Titan Embeddings.

## ⭐ Step 4 — Store in vector DB

(FAISS, OpenSearch, DynamoDB, PGVector, Pinecone)

## ⭐ Step 5 — Query at runtime

Convert user question → embedding → search nearby vectors.

## ⭐ Step 6 — Feed results to LLM (Nova)

Prompt:

```
Use ONLY the context below:
{retrieved_chunks}

Question:
{user_question}
```

## ⭐ Step 7 — LLM generates grounded answer

No hallucinations.

---

# 🎉 **Final Summary — Vector Databases in One View**

| Topic             | Simple Meaning                       |
| ----------------- | ------------------------------------ |
| Vector DB         | Stores meaning of text as numbers    |
| Chunking          | Split documents into small pieces    |
| Embeddings        | Convert text → meaning vectors       |
| Similarity Search | Find closest chunks based on meaning |
| PGVector          | Vector search inside PostgreSQL      |
| Knowledge Base    | AWS managed RAG pipeline             |
| RAG App           | Query → Retrieve → Answer            |

Vector databases are essential for **accurate RAG**, AI chatbots, enterprise search, and modern GenAI applications.

---
