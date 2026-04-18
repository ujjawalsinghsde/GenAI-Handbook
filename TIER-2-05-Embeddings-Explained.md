# TIER 2-05: Embeddings Explained
## Converting Text to Vectors

---

## The Core Idea

An **embedding** is converting text (words, sentences, documents) into a list of numbers (a vector) that represents its meaning.

```
Text: "The cat sat on the mat"
Embedding: [0.2, -0.5, 0.8, 0.1, -0.3, ..., 0.7]  (768 numbers for OpenAI)

Text: "The dog sat on the floor"  
Embedding: [0.2, -0.4, 0.7, 0.2, -0.3, ..., 0.65]  (Similar! Because meanings are similar)

Text: "The fork is sharp"
Embedding: [0.1, 0.3, -0.2, 0.4, 0.1, ..., -0.4]  (Different! Different meaning)
```

**Key insight:** Similar meanings = similar vectors = close distance in vector space.

---

## Why Embeddings Matter

### Problem: Keyword Search is Dumb
```
Search: "How do I fix a broken chair?"

Keyword search finds:
- "chair" (matches!)
- "table" (doesn't match - no "chair" keyword)
- "furniture repair" (doesn't match - no exact keywords)

Result: Miss relevant documents
```

### Solution: Semantic Search with Embeddings
```
Search: "How do I fix a broken chair?"
Embedding: [0.2, -0.5, 0.8, ...]  (represents the meaning)

Compare to:
- "How to repair wooden furniture" → [0.19, -0.52, 0.81, ...] (Very similar!)
- "What tools do I need?" → [0.3, 0.1, 0.5, ...] (Less similar)
- "Photography tips" → [-0.5, 0.8, -0.1, ...] (Completely different)

Result: Find documents by MEANING, not keywords
```

---

## How Embeddings Work

### The Math (Intuitive)

Embeddings are created by neural networks trained on huge amounts of text:

```
Training:
- See word pair: "king" and "queen"
- Learn: These have similar embeddings (both royal)
- See word pair: "king" and "pizza"
- Learn: These have different embeddings (unrelated)

After millions of examples:
- "king" embedding: [0.2, 0.5, 0.8, ...]
- "queen" embedding: [0.18, 0.52, 0.79, ...]  (Very close!)
- "pizza" embedding: [-0.3, -0.1, 0.2, ...]   (Very far!)

This is called "semantic similarity"
```

---

## Dimensions and Size

Embeddings have different sizes:

```
OpenAI (text-embedding-3-small): 1536 dimensions
OpenAI (text-embedding-3-large): 3072 dimensions
Claude (Embedding): 1024 dimensions
Google (Embedding): 768 dimensions
```

**What it means:**
- More dimensions = more information = slower search = better precision
- Fewer dimensions = less information = faster search = less precise

**For most applications:** 768-1536 dimensions is perfect.

---

## Creating Embeddings

### Using OpenAI
```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Embed a text
vector = embeddings.embed_query("What is machine learning?")
print(len(vector))  # 1536 dimensions
print(vector[:5])   # [0.023, -0.012, 0.045, ...]
```

### Using Anthropic
```python
from langchain_anthropic import AnthropicEmbeddings

embeddings = AnthropicEmbeddings(model="claude-embedding-001")

vector = embeddings.embed_query("What is machine learning?")
print(len(vector))  # 1024 dimensions
```

### Using Open Source (Hugging Face)
```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector = embeddings.embed_query("What is machine learning?")
```

---

## Embedding Multiple Documents

```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

documents = [
    "Machine learning is a subset of AI",
    "Deep learning uses neural networks",
    "Natural language processing handles text",
    "Computer vision processes images"
]

# Embed all documents
vectors = embeddings.embed_documents(documents)

print(f"Number of documents: {len(vectors)}")
print(f"Dimensions per document: {len(vectors[0])}")

# Now you can compare them
import numpy as np

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# Compare document 0 and 1
sim = cosine_similarity(vectors[0], vectors[1])
print(f"Similarity between doc0 and doc1: {sim:.3f}")  # 0.8-0.9 (very similar)

# Compare document 0 and 3
sim = cosine_similarity(vectors[0], vectors[3])
print(f"Similarity between doc0 and doc3: {sim:.3f}")  # 0.3-0.4 (less similar)
```

---

## Cosine Similarity (How It Works)

**Cosine similarity** measures how similar two vectors are:

```
Formula: similarity = (v1 · v2) / (|v1| * |v2|)

Result: 1.0  = Identical
        0.8  = Very similar
        0.5  = Somewhat similar
        0.0  = Unrelated
       -1.0  = Opposite
```

**In practice:**
```python
from sklearn.metrics.pairwise import cosine_similarity

v1 = [0.2, 0.5, 0.8]
v2 = [0.2, 0.5, 0.8]  # Identical
v3 = [0.8, 0.5, 0.2]  # Reversed

print(cosine_similarity([v1], [v2]))  # ~1.0 (identical)
print(cosine_similarity([v1], [v3]))  # ~-0.3 (opposite)
```

---

## Real Example: Find Similar Documents

```python
from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

embeddings = OpenAIEmbeddings()

documents = {
    "doc1": "Python is a programming language",
    "doc2": "Java is an object-oriented language",
    "doc3": "Cats are furry animals",
    "doc4": "Dogs are loyal pets",
}

# Embed all
vectors = {
    name: embeddings.embed_query(text)
    for name, text in documents.items()
}

# Find documents similar to a query
query = "What programming languages exist?"
query_vector = embeddings.embed_query(query)

# Score all documents
scores = {}
for name, vector in vectors.items():
    sim = cosine_similarity([query_vector], [vector])[0][0]
    scores[name] = sim

# Sort by relevance
ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

print("Most relevant documents:")
for name, score in ranked:
    print(f"  {name}: {score:.3f}")

# Output:
# doc2: 0.812 (Java is programming language)
# doc1: 0.819 (Python is programming language)
# doc3: 0.234 (cats - unrelated)
# doc4: 0.198 (dogs - unrelated)
```

---

## Practical: Document Similarity Analysis

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

# Load and split documents
loader = PyPDFLoader("document.pdf")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500)
chunks = splitter.split_documents(documents)

# Embed chunks
embeddings = OpenAIEmbeddings()
vectors = [embeddings.embed_query(chunk.page_content) for chunk in chunks]

# Find most similar chunks
def find_similar_chunks(query, top_k=5):
    query_vec = embeddings.embed_query(query)
    
    similarities = [
        (i, cosine_similarity([query_vec], [vec])[0][0])
        for i, vec in enumerate(vectors)
    ]
    
    top = sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
    
    return [(chunks[i].page_content, score) for i, score in top]

# Use it
results = find_similar_chunks("What is machine learning?")
for content, score in results:
    print(f"Score: {score:.3f}")
    print(f"Content: {content[:100]}...")
    print()
```

---

## Embedding Best Practices

### 1. Normalize Your Vectors
```python
import numpy as np

def normalize(vector):
    return vector / np.linalg.norm(vector)

vec = embeddings.embed_query("text")
normalized = normalize(vec)
```

### 2. Cache Embeddings
Don't re-embed the same text:

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_embedding(text):
    return tuple(embeddings.embed_query(text))
```

### 3. Batch Embed When Possible
```python
# Slow: One at a time
for doc in documents:
    vec = embeddings.embed_query(doc)

# Fast: All at once
vectors = embeddings.embed_documents(documents)
```

### 4. Choose Right Model
```
Fast Search:        sentence-transformers/all-MiniLM-L6-v2
Balanced:           text-embedding-3-small (OpenAI)
Best Quality:       text-embedding-3-large (OpenAI)
```

---

## Self-Check

Can you answer:

- [ ] "What is an embedding?" (Text converted to vector of numbers)
- [ ] "Why are embeddings useful?" (Enable semantic search by meaning)
- [ ] "What's cosine similarity?" (Measure of how similar two vectors are)
- [ ] "How do you embed multiple documents?" (embeddings.embed_documents(docs))
- [ ] "When would two embeddings be very similar?" (When texts have similar meaning)

Ready for **[TIER-2-06-Vector-Databases.md](TIER-2-06-Vector-Databases.md)** →

Next: Storing and searching embeddings efficiently.
