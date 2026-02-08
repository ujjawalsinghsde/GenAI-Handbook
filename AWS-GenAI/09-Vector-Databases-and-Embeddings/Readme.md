# Vector Databases

A vector database stores embeddings—numerical vectors representing semantic meaning of text, images, or other content. Vector DBs are foundational for RAG, semantic search, recommendations, and many GenAI systems.

# Introduction to Vector Databases

A vector database stores high-dimensional numeric vectors (embeddings) that represent the meaning of text, images, or other content. Vector DBs are foundational for RAG, semantic search, recommendations, and modern GenAI systems.

Example vector:

```
[0.12, -0.56, 0.33, 0.88, ...]
```

If two vectors are close, their meanings are close.

Simple explanation:

Vector DB = a database that stores embeddings and finds semantically similar items using nearest-neighbor search.

Traditional databases store rows/columns/tables; vector DBs store embeddings, metadata, and meaning-based indexes.

# Use Cases of Vector DBs

Vector databases enable:

- RAG (Retrieval-Augmented Generation): retrieve text chunks for grounded answers.
- Semantic search: find results by meaning rather than keywords.
- Chatbots: answer using PDFs, docs, wikis, and internal systems.
- Recommendations: surface similar products or content.
- Deduplication and clustering: group near-duplicate documents.
- Image search: find visually or semantically similar images.
- Fraud detection: discover similar behavior patterns.
- Personalization: match user profile vectors to content.

# Text Chunking & Embeddings

Before storing data in a vector database, two steps are required: chunking and embedding generation.

---

### Text Chunking

Large documents are split into small, coherent chunks because retrieval and generation perform better on shorter logical segments.

Example:

- PDF → 100 pages
- Chunked into 300–400 text blocks
- ~200–500 words each

Chunk example:

```
"Refund policy for digital products..."
```

Best practices:

- Chunk size: 200–500 tokens
- Overlap: ~50 tokens

---

### Embeddings

Embeddings convert text to numeric vectors.

Example:

```
"Apple the fruit" → [0.12, 0.89, ...]
"Apple the company" → [0.95, 0.11, ...]
```

Different meanings map to distant vectors; similar meanings map to nearby vectors.

Bedrock embedding options:

- Amazon Titan Embeddings v2
- Llama embeddings
- Mistral embeddings

Embeddings capture semantics and are required for semantic search.

# Vector Similarity Search

Similarity search is the core function of a vector database. It returns vectors most similar to a query embedding.

Example query: “How can I cancel a digital order?”

Steps:

1. Convert query → embedding
2. Compare embedding with stored vectors
3. Return the closest matches

Common similarity metrics:

- Cosine similarity
- Dot product
- Euclidean distance

High-quality similarity search supplies relevant context to the model, improving answer accuracy and reducing hallucinations.

---

## Local Vector DB Setup and CRUD Operations

You can run a vector DB locally or in the cloud. Common options include FAISS, Chroma, Milvus, Weaviate, Pinecone, OpenSearch, DynamoDB vector search, and PostgreSQL with pgvector.

### Setup (Example: Chroma local)

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

### Insert embeddings (Create)

```python
collection.add(
    ids=["1"],
    documents=["Refund policy for digital goods..."],
    embeddings=[[0.12, 0.88, ...]]
)
```

---

### Read/Search data (Retrieve)

```python
collection.query(
    query_embeddings=[[0.90, 0.11, ...]],
    n_results=3
)
```

---

### Update embeddings

```python
collection.update(
    ids=["1"],
    documents=["Updated refund policy..."]
)
```

---

### Delete embeddings

```python
collection.delete(ids=["1"])
```

---

# Querying Vector Embeddings

Query flow:

```
User Query → Convert to embedding → Similarity Search → Return relevant chunks
```

Example:

```python
embedding = emb_model.embed_query("What is refund policy?")
res = collection.query(query_embeddings=[embedding], n_results=5)
```

Returned chunks feed into models such as Nova, Claude, Llama, or Mistral for final answer generation.

---

# Amazon PGVector & Embeddings

Amazon Aurora PostgreSQL and RDS PostgreSQL support the `pgvector` extension for storing and searching vectors.

### What is PGVector?

`pgvector` is a Postgres extension that adds a `vector` column type and vector similarity operators for nearest-neighbor search.

### Why it's popular

- Uses familiar relational tooling
- Simple to manage inside a VPC
- Avoids an additional vector service for small-to-medium workloads

### Create a vector table

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE documents (
    id serial PRIMARY KEY,
    content text,
    embedding vector(768)
);
```

### Insert embeddings

```sql
INSERT INTO documents (content, embedding)
VALUES ('Refund policy text', '[0.12, 0.88, ...]');
```

### Search similar embeddings

```sql
SELECT content
FROM documents
ORDER BY embedding <-> '[0.90, 0.11, ...]'
LIMIT 5;
```

The `<->` operator measures vector distance in `pgvector`.

### Embeddings

Use an embedding model (e.g., Amazon Titan) and store `embedding_model` metadata with each vector.

---

# Deep Dive: Amazon Knowledge Bases for Bedrock

The Bedrock Knowledge Base is a managed RAG service that handles ingestion, chunking, embedding, vector storage, retrieval, and generation.

Key managed steps:

- Document ingestion
- Chunking
- Embedding generation
- Vector storage
- Retrieval
- RAG-response generation

Required resources:

- S3 bucket
- Knowledge Base configuration
- Bedrock model (Nova/Claude/Llama)

### Running a query

```python
response = client.retrieve_and_generate(
    knowledgeBaseId="kb-123",
    input={"text": "What is our refund policy?"}
)
```

The service returns retrieved chunks and a grounded generation from the chosen model.

---

# Build a Knowledge Base with a Vector Database

If you prefer to build a knowledge base manually, follow these steps.

### Step 1 — Collect documents

Store source documents in S3, a CMS, or other repositories.

### Step 2 — Chunk documents

Split documents into small, coherent blocks suitable for embedding.

### Step 3 — Generate embeddings

Use a stable embedding model (e.g., Titan) and record the model/version in metadata.

### Step 4 — Store in vector DB

Choose an appropriate vector store (FAISS, OpenSearch, DynamoDB, PGVector, Pinecone) and persist vectors and metadata.

### Step 5 — Query at runtime

Convert the user question to an embedding and perform a nearest-neighbor search to retrieve top-k chunks.

### Step 6 — Feed results to LLM (Nova)

Prompt the LLM using only retrieved context and your instructions:

```
Use ONLY the context below:
{retrieved_chunks}

Question:
{user_question}
```

### Step 7 — LLM generates grounded answer

The model generates answers grounded in the provided context; include citations to sources when possible.

---

---

## Indexing strategies and operational guidance

Indexing and index maintenance are critical for vector search performance, cost, and recall. Use the guidance below when choosing and operating a vector index.

- Index types and algorithms:
    - HNSW (Hierarchical Navigable Small World): high recall and low latency for many open-source vector DBs (Milvus, FAISS HNSW). Tune `M` and `efConstruction` during build and `ef` at query time.
    - IVF / PQ (Inverted File with Product Quantization): compresses vectors for lower storage and faster search at scale; common for FAISS-based systems.
    - Annoy / KD-Tree: useful for read-heavy, static datasets; less suitable for frequent updates.

- Distance / similarity metric:
    - Choose `cosine` or `dot` for embedding vectors from most LLM providers; `L2` (Euclidean) is sometimes used depending on model output.
    - Normalize embeddings when using cosine similarity (unit vectors) to keep metric behavior consistent.

- Index parameters and tuning:
    - For HNSW: set `M` (connectivity) and `efConstruction` (build-time search breadth). Higher values increase build time and memory but improve recall.
    - For IVF/PQ: choose `nlist` (# of centroids) and PQ code size for trade-offs between speed and accuracy.
    - Query-time knobs: `ef` or `probe` and `k` (top-k results). Increase `ef` to improve recall at cost of latency.

- Ingestion patterns:
    - Batch ingestion for initial bulk loads with index build/optimize step.
    - Streaming / incremental upserts: use append + periodic rebalancing or background index merge for systems that support it (e.g., Milvus). Avoid rebuilding full index on every small update.
    - Use tombstones or soft-deletes for safe deletion semantics; periodically compact the index.

- Embedding and index versioning:
    - Store `embedding_model` and `embedding_version` in metadata for each vector to support reindexing when models change.
    - Maintain a reindex plan: incremental re-embed changed documents, or schedule full reindex when switching major embedding models.

- Metadata schema (recommended fields):
    - `id` (unique vector id)
    - `source` (S3 path, URL, or system)
    - `document_id`, `chunk_id`, `page`, `offset`
    - `embedding_model`, `embedding_version`
    - `language`, `mime_type`, `tags`
    - `created_at`, `updated_at`, `checksum`

- Deduplication and normalization:
    - Normalize whitespace, remove boilerplate, canonicalize dates and numeric formats before chunking.
    - Deduplicate near-identical chunks (use a secondary fingerprint or similarity threshold) to reduce index size and noise.

- Backups, snapshots and disaster recovery:
    - Take regular snapshots of vector indexes and metadata (where supported). For managed services use their snapshot APIs.
    - Store snapshots in S3 with lifecycle policies and cross-region replication if needed.

- Monitoring and observability:
    - Track query latency, throughput, recall@k, and index build times.
    - Log top-k vectors returned per query (ids and scores) for offline evaluation and drift detection.
    - Alert on increases in average query latency or sudden drops in recall metrics.

- Security and access control:
    - Restrict network access (VPC, security groups) and use IAM for service principals.
    - Encrypt embeddings at rest and in transit; redact sensitive fields from stored metadata.

- Cost considerations:
    - Index size grows with vector dimensionality and number of vectors; balance embedding dimension vs model quality.
    - Use compression (PQ) or quantization when storage/IO cost is a concern.

- Sample operational checklist:
    1. Define metadata schema and embedding model contract.
    2. Validate documents and normalize text before chunking.
    3. Choose index type (HNSW/IVF/PQ) and test recall/latency trade-offs on representative workload.
    4. Implement incremental ingestion with periodic reindex windows.
    5. Snapshot indexes and metadata daily; test restores quarterly.
    6. Monitor recall@k, latency, and query patterns; tune parameters when needed.

---

# Final Summary — Vector Databases in One View

| Topic             | Simple Meaning                       |
| ----------------- | ------------------------------------ |
| Vector DB         | Stores meaning of text as numbers    |
| Chunking          | Split documents into small pieces    |
| Embeddings        | Convert text → meaning vectors       |
| Similarity Search | Find closest chunks based on meaning |
| PGVector          | Vector search inside PostgreSQL      |
| Knowledge Base    | AWS managed RAG pipeline             |
| RAG App           | Query → Retrieve → Answer            |

Vector databases are essential for accurate RAG, AI chatbots, enterprise search, and modern GenAI applications.

---
