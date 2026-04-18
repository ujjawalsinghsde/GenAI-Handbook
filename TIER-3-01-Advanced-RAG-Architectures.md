# TIER 3-01: Advanced RAG Architectures
## Beyond Basic Retrieval

---

## The Problem with Simple RAG

### Issue 1: Poor Retrieval
```
Query: "How do I reset my password?"
Retrieved chunks: [Unrelated content from FAQ]
Result: ❌ Wrong information
```

### Issue 2: Lost Context
```
Query: "What about that policy I just asked?"
System: "Doesn't remember previous questions"
Result: ❌ Repeated context for each query
```

### Issue 3: Token Limits
```
Query: Long question
Retrieved: 10 relevant chunks (3000 tokens)
LLM context: Only 4K tokens
Result: ❌ Exceeds limit
```

### Issue 4: Ranking Irrelevance
```
Retrieved: [Relevant, Somewhat Relevant, Irrelevant, Irrelevant, Relevant]
LLM sees: All 5 equally
Result: ❌ Confused by bad matches
```

**Advanced RAG solves these problems.**

---

## Architecture 1: Hierarchical Retrieval

### Problem Solved
Different queries need different chunk sizes.
- "Give me a quick overview" → Large chunks
- "What specific date was mentioned?" → Small chunks

### Solution

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# Create two vector stores: summaries (large) + details (small)
summary_chunks = split_with_size(documents, chunk_size=2000)
detail_chunks = split_with_size(documents, chunk_size=500)

summary_store = Chroma.from_documents(summary_chunks, embeddings)
detail_store = Chroma.from_documents(detail_chunks, embeddings)

# Route queries
def get_chunks(query):
    if "summary" in query.lower():
        return summary_store.as_retriever()
    else:
        return detail_store.as_retriever()
```

---

## Architecture 2: Hierarchical Indexing (Tree Retrieval)

### How It Works

```
Documents
    ↓
Create summaries of each document
    ↓
Index documents + summaries
    ↓
Search summaries first (fast)
    ↓
Retrieved summaries point to full documents
    ↓
Get specific details from full documents

Result: Fast initial search + precise details
```

### Implementation

```python
from langchain.chains.summarize import load_summarize_chain

# Create summaries
summarize_chain = load_summarize_chain(llm, chain_type="map_reduce")
summaries = summarize_chain.run(documents)

# Index both
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import InMemoryStore

# Store mapping: summary → full document
store = InMemoryStore()
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    byte_store=store,
    id_key="doc_id"
)

# Now retrieve gets full documents using summaries!
relevant_docs = retriever.get_relevant_documents("query")
```

---

## Architecture 3: Multi-Query Retrieval

### Problem
Single query might miss relevant documents.

```
Query: "password reset"
Missed: Documents about "authentication" or "account recovery"
```

### Solution: Expand the Query

```python
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI

# Ask LLM to generate related queries
retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=ChatOpenAI(model="gpt-4"),
    prompt=... # Tell it to generate 3 variations
)

# Queries generated:
# 1. "How do I reset my password?"
# 2. "Password recovery process?"
# 3. "What if I forgot my login credentials?"

results = retriever.get_relevant_documents("How do I reset my password?")
# Gets results from ALL queries!
```

---

## Architecture 4: Hybrid Search (BM25 + Vector)

### Why Both?
```
Vector search: Great for meaning ("financial planning" → money concepts)
Keyword search: Great for exact terms ("API endpoint" → exact match)

Combined: Get both semantic + exact matches!
```

### Implementation

```python
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

# Vector retriever (semantic)
vector_retriever = vectorstore.as_retriever()

# BM25 retriever (keyword)
bm25_retriever = BM25Retriever.from_documents(documents)

# Combine them
ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.6, 0.4]  # 60% semantic, 40% keyword
)

# Use ensemble
docs = ensemble_retriever.get_relevant_documents("query")
```

---

## Architecture 5: Re-Ranking Retrieved Results

### Problem
Retrieved docs aren't necessarily in best order.

```
Retrieved:
1. Somewhat relevant (score 0.75)
2. Highly relevant (score 0.73) ← Should be first!
3. Somewhat relevant (score 0.72)
```

### Solution: Re-rank with LLM

```python
from langchain_community.document_compressors import LLMListwiseReranker
from langchain.retrievers import ContextualCompressionRetriever

# Reranker (uses LLM to judge relevance)
reranker = LLMListwiseReranker(llm=ChatOpenAI(model="gpt-4"))

# Wrap retriever
compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=vectorstore.as_retriever()
)

# Use it - results are now ranked!
docs = compression_retriever.get_relevant_documents("query")
```

---

## Architecture 6: Query Expansion with Metadata Filtering

### How It Works

```
Query: "How do I cancel?"
↓
Determine context: Financial product
↓
Filter to financial documents only
↓
Search within filtered set

Result: More relevant results
```

### Implementation

```python
def contextual_retrieval(query, context_type):
    # Route to appropriate retriever based on context
    filters = {
        "billing": {"category": "billing"},
        "technical": {"category": "technical"},
        "general": {}
    }
    
    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k": 5,
            "filter": filters.get(context_type, {})
        }
    )
    
    return retriever.get_relevant_documents(query)

# Use it
docs = contextual_retrieval("How do I cancel?", context_type="billing")
```

---

## Architecture 7: Conversation Memory with RAG

### Problem
```
Turn 1: "What's the return policy?"
        LLM retrieves return policy docs

Turn 2: "How long do I have?"
        LLM forgot previous context!
```

### Solution: Add Memory

```python
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain.chains import RetrievalQA

memory = ConversationBufferMemory(return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{question}"),
    ("system", "Retrieved docs: {context}")
])

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(),
    chain_type="stuff",
    retriever=retriever,
    memory=memory
)

# Now it remembers!
qa_chain.invoke("What's the return policy?")
qa_chain.invoke("How long do I have?")  # Knows it's about returns
```

---

## Architecture 8: Routing Queries to Specialized Retrievers

### Problem
```
Different queries need different sources:
- "What's our company culture?" → HR docs
- "API documentation?" → Technical docs
- "Where's our office?" → General info
```

### Solution: Route to Specialized Retrievers

```python
from langchain_core.runnables import RunnableBranch

# Create specialized retrievers
hr_retriever = Chroma(..., persist_directory="./hr_db").as_retriever()
tech_retriever = Chroma(..., persist_directory="./tech_db").as_retriever()
general_retriever = Chroma(..., persist_directory="./general_db").as_retriever()

# Router function
def route_query(query):
    if any(word in query.lower() for word in ["culture", "team", "hr", "people"]):
        return hr_retriever
    elif any(word in query.lower() for word in ["api", "code", "technical"]):
        return tech_retriever
    else:
        return general_retriever

# Create routing chain
retriever = RunnableBranch(
    (lambda x: "api" in x.lower(), tech_retriever),
    (lambda x: "culture" in x.lower(), hr_retriever),
    general_retriever
)

# Use it - automatically routes!
docs = retriever.invoke("What's the API endpoint?")
```

---

## Combining Architectures (Production Setup)

```
User Query
    ↓
1. EXPANSION: Multi-query expansion
    ↓
2. ROUTING: Send to specialized retriever (HR/Tech/General)
    ↓
3. FILTERING: Filter by metadata
    ↓
4. HYBRID SEARCH: BM25 + Vector
    ↓
5. RE-RANKING: LLM reranks top 10
    ↓
6. MEMORY: Add conversation context
    ↓
7. GENERATION: LLM generates answer
    ↓
Answer (high quality, context-aware, relevant)
```

---

## Real Code: Advanced RAG

```python
from langchain_core.runnables import RunnableBranch
from langchain.retrievers import MultiQueryRetriever
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_community.document_compressors import LLMListwiseReranker
from langchain.retrievers import ContextualCompressionRetriever

class AdvancedRAG:
    def __init__(self, llm, documents, metadata):
        self.llm = llm
        self.documents = documents
        
        # Multi-query retriever
        self.multi_retriever = MultiQueryRetriever.from_llm(
            retriever=vectorstore.as_retriever(),
            llm=llm
        )
        
        # BM25 retriever
        self.bm25 = BM25Retriever.from_documents(documents)
        
        # Ensemble
        self.ensemble = EnsembleRetriever(
            retrievers=[self.multi_retriever, self.bm25],
            weights=[0.7, 0.3]
        )
        
        # Re-ranker
        self.reranker = LLMListwiseReranker(llm=llm)
        self.compression = ContextualCompressionRetriever(
            base_compressor=self.reranker,
            base_retriever=self.ensemble
        )
    
    def retrieve(self, query):
        """Get best documents for query"""
        return self.compression.get_relevant_documents(query)
    
    def answer(self, query):
        """Get answer with advanced retrieval"""
        docs = self.retrieve(query)
        
        # Use retrieved docs in generation
        context = "\n".join([d.page_content for d in docs])
        
        prompt = f"""Context: {context}
        
        Question: {query}
        
        Answer based only on the context:"""
        
        return self.llm.invoke(prompt)

# Use it
advanced_rag = AdvancedRAG(llm, documents, metadata)
answer = advanced_rag.answer("What's the return policy?")
```

---

## When to Use Each

| Architecture | When | Example |
|---|---|---|
| Hierarchical | Variable query complexity | "Summary" vs "details" |
| Multi-Query | Topic varies | "password"/"login"/"authentication" |
| Hybrid | Need exact + semantic | Financial queries, regulations |
| Re-ranking | Low retrieval quality | FAQ with many similar items |
| Routing | Multiple knowledge bases | HR docs + Tech docs |
| Memory | Multi-turn conversation | Customer support chatbot |

---

## Self-Check

Can you explain:

- [ ] "Why is simple retrieval not enough?" (Misses context, poor ranking)
- [ ] "What does multi-query do?" (Expands one query into many variations)
- [ ] "How does hybrid search work?" (Combines keyword + semantic)
- [ ] "Why re-rank?" (Reorder results by relevance)
- [ ] "When use hierarchical?" (Variable complexity queries)

Ready for **[TIER-3-02-Tools-and-Function-Calling.md](TIER-3-02-Tools-and-Function-Calling.md)** →

Next: Making LLMs take actions.
