# TIER 2-06: Vector Databases
## Storing and Searching Embeddings

---

## The Problem: Searching Many Vectors

If you have 1 million documents (1 million embeddings), how do you find the most similar to a query?

```
Naive approach:
1. For each of 1 million embeddings
2. Calculate similarity to query
3. Return top 10

Time: ~1 second (too slow!)
```

**Vector databases solve this** with special indexing (like a library card system).

```
Vector database approach:
1. Look up in index
2. Get top 10 in milliseconds

Time: ~10 milliseconds (much better!)
```

---

## Popular Vector Databases

### Cloud-Based

**Pinecone**
- Easiest to use
- Managed service
- Good free tier

**Weaviate**
- Open source + cloud
- Good community

**Supabase (pgvector)**
- PostgreSQL with vectors
- Cheap, good for small projects

### Open Source / Self-Hosted

**Chroma**
- Lightweight, local
- Perfect for learning
- No infrastructure needed

**Milvus**
- Scalable, production-ready
- Self-hosted

**Qdrant**
- Modern, fast
- Good for production

---

## Using Chroma (Local, Easy)

### Setup
```bash
pip install chromadb langchain-community
```

### Create and Store Embeddings
```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Documents
documents = [
    "Python is a programming language",
    "Java is object-oriented",
    "Cats are furry animals",
    "Dogs are loyal pets",
]

# Create vector store
vectorstore = Chroma.from_texts(
    documents=documents,
    embedding=OpenAIEmbeddings(),
    persist_directory="./chroma_db"  # Save to disk
)

print(f"Stored {len(vectorstore)} documents")
```

### Search (Semantic Search)
```python
# Search for similar documents
query = "What programming languages exist?"
results = vectorstore.similarity_search(query, k=2)

for doc in results:
    print(doc.page_content)
    print()

# Output:
# Python is a programming language
# Java is object-oriented
```

### Search with Scores
```python
# Get similarity scores
results = vectorstore.similarity_search_with_scores(query, k=2)

for doc, score in results:
    print(f"Score: {score:.3f}")
    print(f"Content: {doc.page_content}")
    print()
```

---

## Loading and Persisting Data

### Save to Disk
```python
vectorstore = Chroma.from_texts(
    documents,
    embedding=OpenAIEmbeddings(),
    persist_directory="./my_db"
)

# Automatically saved!
```

### Load from Disk
```python
vectorstore = Chroma(
    persist_directory="./my_db",
    embedding_function=OpenAIEmbeddings()
)

# Access stored documents
results = vectorstore.similarity_search("query")
```

---

## Using Pinecone (Cloud)

### Setup
```bash
pip install pinecone-client
```

### Store Embeddings
```python
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings
import pinecone

# Initialize Pinecone
pinecone.init(
    api_key="your-api-key",
    environment="us-west1-gcp"
)

# Create index
if "index-name" not in pinecone.list_indexes():
    pinecone.create_index("index-name", dimension=1536)

# Store documents
vectorstore = Pinecone.from_texts(
    texts=documents,
    embedding=OpenAIEmbeddings(),
    index_name="index-name"
)
```

### Search
```python
results = vectorstore.similarity_search("query", k=5)

for doc in results:
    print(doc.page_content)
```

---

## Advanced: Metadata and Filtering

### Add Metadata to Documents
```python
from langchain_core.documents import Document

documents = [
    Document(
        page_content="Python is a programming language",
        metadata={"type": "tutorial", "language": "python"}
    ),
    Document(
        page_content="Java is object-oriented",
        metadata={"type": "tutorial", "language": "java"}
    ),
    Document(
        page_content="Cats are furry animals",
        metadata={"type": "facts", "category": "animals"}
    ),
]

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=OpenAIEmbeddings()
)
```

### Filter by Metadata
```python
# Find programming tutorials only
results = vectorstore.similarity_search_with_filter(
    query="programming",
    filter={"type": "tutorial"}
)

# In Pinecone:
# results = vectorstore.similarity_search(
#     query="programming",
#     k=5,
#     filter={"type": {"$eq": "tutorial"}}
# )
```

---

## Vector Store as Retriever

### Convert to Retriever
```python
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}  # Return top 5
)

# Now use in chains
docs = retriever.invoke("What programming languages exist?")
```

### Custom Retriever Settings
```python
retriever = vectorstore.as_retriever(
    search_type="similarity",  # or "mmr" for diversity
    search_kwargs={
        "k": 5,
        "filter": {"type": "tutorial"}
    }
)
```

---

## Real Example: Document Q&A

```python
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# 1. Load documents
loader = PyPDFLoader("document.pdf")
documents = loader.load()

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500)
chunks = splitter.split_documents(documents)

# 3. Create vector store
vectorstore = Chroma.from_documents(
    chunks,
    OpenAIEmbeddings(),
    persist_directory="./db"
)

# 4. Create retriever
retriever = vectorstore.as_retriever()

# 5. Create Q&A chain
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4"),
    chain_type="stuff",
    retriever=retriever
)

# 6. Ask questions
answer = qa.invoke("What is the main topic?")
print(answer)
```

---

## Performance: Comparison

| Database | Speed | Scalability | Setup | Cost |
|----------|-------|-------------|-------|------|
| Chroma | Fast | Local only | 1 min | Free |
| Pinecone | Very Fast | ∞ | 5 min | $| 
| Weaviate | Fast | High | 10 min | Varies |
| Milvus | Very Fast | High | 30 min | Free |

---

## Best Practices

### 1. Choose Right Chunk Size
```python
# Too small (100 tokens)
splitter = RecursiveCharacterTextSplitter(chunk_size=100)
# Result: Many small chunks, searches take longer

# Too large (2000 tokens)
splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
# Result: Few large chunks, lose precision

# Just right (500 tokens)
splitter = RecursiveCharacterTextSplitter(chunk_size=500)
```

### 2. Use Overlap for Context
```python
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100  # Overlap to preserve context
)
```

### 3. Index Once, Query Many Times
```python
# Don't recreate the index every time
vectorstore = Chroma(
    persist_directory="./db",
    embedding_function=OpenAIEmbeddings()
)

# Use it multiple times
for question in questions:
    results = vectorstore.similarity_search(question)
```

### 4. Monitor Vector Quality
```python
# Check similarity scores
results = vectorstore.similarity_search_with_scores(
    query,
    k=10
)

for doc, score in results:
    if score < 0.7:  # Low similarity threshold
        print(f"Warning: Low similarity {score:.2f}")
```

---

## Self-Check

Can you answer:

- [ ] "Why do we need vector databases?" (Efficient search of embeddings)
- [ ] "What's the difference between Chroma and Pinecone?" (Chroma=local/free, Pinecone=cloud/managed)
- [ ] "How do you store documents in a vector store?" (Chroma.from_documents())
- [ ] "How do you search?" (vectorstore.similarity_search())
- [ ] "What's chunk_overlap?" (Overlapping text to preserve context between chunks)

Ready for **[TIER-2-07-RAG-From-First-Principles.md](TIER-2-07-RAG-From-First-Principles.md)** →

Next: Putting it all together - RAG systems.
