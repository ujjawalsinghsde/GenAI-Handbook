# Retrieval-Augmented Generation (RAG)

RAG combines document retrieval with language generation so LLMs answer using external, company-owned knowledge stores. This reduces hallucinations and supports up-to-date, auditable responses.

## What RAG Does

- Retrieves relevant document chunks for a user query
- Supplies retrieved context to the model for grounded generation
- Returns answers with source attribution when possible

## High-Level Pipeline

Documents → Chunking → Embeddings → Vector Store → Retrieval → Model → Answer

Example scenario: a user asks for a company policy; the system retrieves the policy text from S3 or SharePoint and uses it as context for the model to generate a factual response.

# Why RAG is Important

RAG addresses key limitations of standalone LLMs by grounding answers in company-controlled documents. The benefits below explain why RAG is widely used in production.

## Avoids Hallucinations

LLMs can produce plausible-sounding but incorrect statements. RAG reduces hallucinations by supplying real documents as context for generation.

## Uses Latest, Private, Company-Specific Knowledge

LLM training data can be stale or non-enterprise. RAG enables use of up-to-date internal documents, policies, and real-time business data.

## No Need to Fine-Tune Model

Rather than fine-tuning, use the RAG pattern: store documents, generate embeddings, and retrieve relevant chunks at query time. This reduces cost and iteration time.

## Cost and Speed

RAG often costs far less than fine-tuning large models because it focuses compute at retrieval and generation time rather than full model re-training.

## Model Agnostic

RAG works with any LLM (Nova, Claude, Llama, Mistral) because retrieval and embedding layers are decoupled from the generator.

## Maintenance

Update documents and re-embed changed content; you do not need to retrain the LLM.

# Building RAG Applications with Amazon Nova

Amazon Nova + Bedrock make RAG simple and enterprise-ready. The high-level architecture below describes common deployment choices and where each component runs.

---

### The RAG Pipeline (Simple Diagram)

```
Documents → Chunking → Embeddings → Vector Store → Retrieval → Nova Model → Answer
```

Let’s break each step.

---

### Step-by-Step RAG Workflow

#### Step 1 — Collect Documents

Documents are commonly stored in:

- S3
- SharePoint
- Websites
- Wikis
- PDFs

---

#### Step 2 — Chunking

Large documents are broken into small parts.

Example:
PDF of 100 pages → chunked into 200 short pieces.

Why?
LLMs work better with smaller text pieces.

---

#### Step 3 — Create Embeddings

Each chunk is converted into a numeric vector representation.

Using Titan Embeddings on Bedrock:

```python
from langchain_aws import BedrockEmbeddings
emb = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2")
```

Embeddings capture semantic meaning beyond surface words.

---

#### Step 4 — Store Embeddings in a Vector Database

AWS options include:

- OpenSearch
- DynamoDB with vector support
- Aurora PostgreSQL with pgvector
- Bedrock Knowledge Base (managed)

Vector DB enables semantic search: find chunks similar in meaning to a query.

---

#### Step 5 — Retrieve Relevant Chunks

At query time:

- Convert the question into an embedding
- Search nearest vectors
- Retrieve the top-k results

---

#### Step 6 — Send Docs + Question to Nova

Prompt example:

```
Use ONLY the provided context to answer the question.
Context:
{retrieved_chunks}

Question:
{user_question}

If answer not found in context, say: "Not available in the documents."
```

Nova (Pro or Lite) generates the grounded answer based on retrieved context.

---

### Using Bedrock Knowledge Base (Recommended)

AWS offers a fully managed Knowledge Base service that handles document ingestion, chunking, embedding generation, vector storage, and retrieval. Use it when you want lower operational overhead.

Example API:

```python
client.retrieve_and_generate(
  input={"text": "What is our digital refund policy?"},
  knowledgeBaseId="kb-12345"
)
```

The service returns retrieved context and a grounded generation from Nova.

---

### RAG with Nova Pro (Multimodal RAG)

Nova Pro supports multimodal inputs including text chunks, images, PDF snapshots, and video frames. This enables RAG that uses visual and textual context together.

Example: upload a PDF with diagrams and images; Nova can reason over both text and visual content.

---

## Embeddings and RAG System Design

Embeddings are the core of RAG systems; they map content to numeric vectors that capture semantic meaning.

---

### What Are Embeddings? (Simple Explanation)

Embeddings are numeric representations of meaning. For example, "dog" and "puppy" will have nearby vectors, while "dog" and "laptop" will be distant.

---

### Why Embeddings Matter in RAG

RAG relies on semantic similarity: the system must retrieve chunks whose embeddings are closest in meaning to the query (refund policy, cancellation instructions, etc.).

---

### Embedding Model Options (Bedrock)

Bedrock supports multiple embedding providers including Titan, Mistral, and Llama variants. Titan embeddings are a common default for AWS environments and multilingual workloads.

---

### Chunking Strategy

Chunk size affects retrieval quality. Best practices:

- Use 200–500 token chunks
- Overlap chunks by ~50 tokens
- Store metadata (document title, page number, source)

Better chunking improves retrieval and final answer quality.

---

### Vector Store Design

Consider query latency, scalability, cost, and consistency when choosing a vector store. AWS options include OpenSearch Vector, DynamoDB vector support, Aurora with pgvector, or Bedrock Knowledge Base.

---

### Retrieval Techniques

Common techniques:

- Top-k retrieval (k=3..5)
- Re-ranking retrieved chunks
- Hybrid search combining keyword and vector search for improved relevance

---

### Prompt Template for RAG

```
You are an AI assistant. Use ONLY the provided context.

Context:
{docs}

Question:
{query}

If information is missing, say "Not available in the documents."
```

---


## Evaluation Metrics for RAG

Monitor the retrieval and generation pipeline separately:

- Retrieval: precision@k, recall, mean reciprocal rank (MRR), and relevance judged by humans
- Generation: answer accuracy, faithfulness, and citation correctness
- Operational: latency, throughput, and cost per query

## Production Considerations

- **Provenance and Citation**: always return source identifiers (document id, page, offset) with answers to enable user verification.  
- **Deduplication & Normalization**: dedupe document chunks and normalize text before embedding.
- **Freshness**: implement incremental ingestion and re-indexing strategies for updated documents.  
- **Ingestion Pipeline**: validate documents, normalize text, extract metadata, apply chunking, and version embeddings.  
- **Retriever Monitoring**: log top-k retrieved items, track whether retrieved items contain ground-truth answers, and set alerts for drops in retrieval quality.  
- **Fallbacks and Safety**: return explicit 'not found' responses if no reliable context is available; avoid confident guessing.  
- **Access Controls**: enforce access policies on vector stores and knowledge bases to protect sensitive data.

### Indexing, embedding versioning, and maintenance

Index management and embedding versioning are essential parts of a reliable RAG system. Add the following operational controls to your pipeline:

- Embedding model contract: record `embedding_model` and `embedding_version` with each vector so you can identify which vectors were produced by which encoder.
- Reindexing strategy: prefer incremental re-embedding for changed documents and schedule full reindexes only when necessary (major model or schema changes). Maintain a reindex job plan and a migration window.
- Index naming and namespaces: include environment and model-version in index names (e.g., `prod_docs_titan_v2_v1`) to avoid accidental mixing of vectors from different models.
- Upserts & deletes: design safe upsert patterns (idempotent operations) and use tombstone markers for deletes; compact or rebuild periodically depending on storage engine.
- Index tuning: expose index parameters (e.g., HNSW `M`/`efConstruction`, IVF `nlist`, query `ef`) in config and track their impact on recall and latency.

### Metadata, provenance and citation (detailed)

High-quality provenance makes RAG auditable and trustworthy. Recommended metadata fields and practices:

- Required fields: `document_id`, `chunk_id`, `source`, `page`, `offset`, `score`, `embedding_model`, `embedding_version`.
- Optional: `language`, `author`, `checksum`, `ingest_batch_id`, `ingested_at`.
- Citation format: return a compact citation with each answer, e.g. `{source: 's3://bucket/path.pdf', page: 12, chunk_id: 'doc123#c45'}` and surface these to users or in logs.
- Verifiability: store raw chunk offsets and checksums so users can fetch the exact source text during audits.

### Monitoring and evaluation

- Retrieval metrics: precision@k, recall@k, MRR, and average score of top-k.
- Drift detection: monitor distribution of query-to-vector distances and embedding score histograms to detect embedding-model drift.
- A/B evaluation: when changing embedding models or index parameters, run A/B tests on a holdout set to measure retrieval + generation quality before full rollout.

### Operational checklist (RAG)

1. Define metadata contract and index naming conventions.
2. Implement normalized chunking and deduplication during ingestion.
3. Store embedding model/version with vectors and keep a reindex plan.
4. Choose and test index type (HNSW/IVF/PQ) on representative data.
5. Implement incremental ingestion with batch reindex windows.
6. Log top-k retrievals and source citations for offline QA.
7. Monitor recall and latency; alert on regressions.
8. Ensure access controls and encrypted storage for vectors and documents.

## Summary

RAG is a production pattern that grounds model responses in external knowledge. Focus on provenance, retrieval quality, monitoring, and secure ingestion to build reliable, auditable systems.
