# TIER 2-01: Introduction to LangChain
## Why This Framework Exists and What It Solves

---

## The Problem: Building LLM Apps is Hard

Imagine you want to build a chatbot. Here's what you need to do manually:

```python
# Without LangChain (bare minimum):
import openai

# Handle API authentication
openai.api_key = "your-key"

# Call the API
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)

# Parse response
answer = response['choices'][0]['message']['content']

# Handle errors
# Handle retries
# Handle rate limiting
# Handle token counting
# Build memory for conversations
# Load documents
# Split documents
# Create embeddings
# Store in vector database
# Search and retrieve
# Parse structured output
# ... and much more
```

**This is just for a simple call.** Real applications need:
- Prompt templates (reusable prompts)
- Chains (multiple steps connected)
- Memory (remember conversation history)
- Document loading and splitting
- Embeddings and vector storage
- RAG workflows
- Error handling and retries
- Logging and monitoring

**That's a LOT of boilerplate code.**

---

## What is LangChain?

**LangChain** is a Python/JavaScript framework that handles all this boilerplate.

**Simple definition:** A toolkit that makes building LLM applications easier.

**Like:** 
- Django for web development
- Flask for simple APIs
- NumPy for data science

It provides pre-built components you can snap together.

---

## What LangChain Gives You

### 1. **LLM Wrappers (Models)**
Connect to any LLM easily:

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

# OpenAI
llm = ChatOpenAI(model="gpt-4")

# Anthropic (Claude)
llm = ChatAnthropic(model="claude-3-sonnet")

# Same interface, different models
response = llm.invoke("What is AI?")
```

**Benefit:** Switch models without rewriting code.

### 2. **Prompt Templates**
Reusable prompts with variables:

```python
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert {expertise}."),
    ("user", "Explain {topic} in simple terms.")
])

# Use multiple times with different variables
prompt1 = template.invoke({"expertise": "physicist", "topic": "quantum mechanics"})
prompt2 = template.invoke({"expertise": "biologist", "topic": "photosynthesis"})
```

**Benefit:** DRY (Don't Repeat Yourself) for prompts.

### 3. **Chains**
Connect multiple operations in sequence:

```python
from langchain_core.runnables import RunnableSequence

# Step 1: Create prompt
# Step 2: Call LLM
# Step 3: Parse output
# Step 4: Do something with result

chain = prompt | llm | output_parser
result = chain.invoke({"topic": "AI"})
```

**Benefit:** Complex workflows become simple.

### 4. **Memory**
Automatically manage conversation history:

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()

# Automatically stores conversation
memory.chat_memory.add_user_message("Hello")
memory.chat_memory.add_ai_message("Hi there!")

# Retrieves when needed
history = memory.chat_memory.messages
```

**Benefit:** Multi-turn conversations work automatically.

### 5. **Document Loaders**
Load documents from various sources:

```python
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader

# Load PDF
pdf_docs = PyPDFLoader("document.pdf").load()

# Load webpage
web_docs = WebBaseLoader("https://example.com").load()

# Load from database, S3, local files, etc.
```

**Benefit:** Work with documents without writing custom code.

### 6. **Text Splitters**
Break large documents into chunks:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)
# Result: [Document1, Document2, Document3, ...]
```

**Benefit:** Automatic, intelligent chunking.

### 7. **Vector Stores**
Store and search embeddings:

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Create vector store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=OpenAIEmbeddings()
)

# Search
results = vectorstore.similarity_search("What is machine learning?", k=5)
```

**Benefit:** Semantic search in 3 lines of code.

### 8. **Retrievers**
Find relevant documents automatically:

```python
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}  # Return top 5
)

docs = retriever.invoke("What is AI?")
```

**Benefit:** Abstraction over vector search.

### 9. **Output Parsers**
Convert LLM output to structured data:

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser()

# LLM returns: '{"name": "John", "age": 30}'
# Parser converts to: {"name": "John", "age": 30}

result = parser.invoke(llm_output)
```

**Benefit:** Unstructured LLM output → structured data.

### 10. **RAG Systems**
Built-in retrieval-augmented generation:

```python
from langchain.chains import RetrievalQA

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

answer = qa.invoke("What is in the documents?")
```

**Benefit:** RAG in 5 lines of code.

---

## The LangChain Ecosystem

```
langchain (core library)
    ├── langchain-openai (OpenAI models)
    ├── langchain-anthropic (Claude models)
    ├── langchain-google (Gemini models)
    ├── langchain-community (300+ integrations)
    └── langgraph (agentic workflows)
```

**Everything works together seamlessly.**

---

## Real Example: Build a Q&A Bot in 20 Lines

Without LangChain:
```python
# 100+ lines of boilerplate code
```

With LangChain:
```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# Load documents
documents = PyPDFLoader("company_docs.pdf").load()

# Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
chunks = splitter.split_documents(documents)

# Create vector store
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=OpenAIEmbeddings()
)

# Create Q&A chain
qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4"),
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Use it!
answer = qa.invoke("What is our company's policy on remote work?")
print(answer)
```

**20 lines. That's it.**

---

## Key Concepts in LangChain

### **Runnable Interface**
Everything in LangChain is a "Runnable". They have a consistent interface:

```python
# All of these work the same way:
llm.invoke(input)          # Call LLM
prompt.invoke(input)       # Create prompt
chain.invoke(input)        # Run chain
retriever.invoke(input)    # Retrieve docs

# They all return output
```

**Benefit:** Consistency. Learn one pattern, use everywhere.

### **Composition**
Chain operations together with `|` (pipe):

```python
# Instead of:
prompt_out = prompt.invoke(input)
llm_out = llm.invoke(prompt_out)
parser_out = parser.invoke(llm_out)

# You write:
chain = prompt | llm | parser
result = chain.invoke(input)
```

**Benefit:** Readable, functional programming style.

### **Streaming**
Get responses as they're generated:

```python
for chunk in chain.stream(input):
    print(chunk, end="", flush=True)
```

**Benefit:** Responsive UI, immediate feedback.

---

## LangChain Architecture

```
Your Application
      ↓
LangChain (high level)
  ├── Chains
  ├── Agents
  ├── RAG
      ↓
LangChain Core (medium level)
  ├── Prompts
  ├── Runnables
  ├── Output Parsers
      ↓
LangChain Community (low level)
  ├── LLM Wrappers (OpenAI, Claude, etc.)
  ├── Document Loaders (PDF, Web, etc.)
  ├── Vector Stores (Chroma, Pinecone, etc.)
  ├── Memory Management
      ↓
External Services
  ├── OpenAI API
  ├── Anthropic API
  ├── Embedding Service
  ├── Vector Database
```

---

## Why Use LangChain? (The Real Benefits)

### 1. **Speed**
Build in hours instead of days.

### 2. **Less Boilerplate**
Focus on logic, not infrastructure.

### 3. **Flexibility**
Easy to switch models, databases, etc.

### 4. **Community**
300+ integrations, active community.

### 5. **Production Ready**
Error handling, retries, logging built-in.

### 6. **Pythonic**
Clean, readable code.

---

## What You'll Learn in TIER 2

| Document | Focus |
|----------|-------|
| [TIER-2-01](TIER-2-01-Introduction-to-LangChain.md) | Why LangChain exists |
| [TIER-2-02](TIER-2-02-Models-and-LLM-Invocation.md) | Call LLMs through LangChain |
| [TIER-2-03](TIER-2-03-Prompts-and-Templates.md) | Reusable prompts |
| [TIER-2-04](TIER-2-04-Chains.md) | Connect operations |
| [TIER-2-05](TIER-2-05-Embeddings-Explained.md) | Convert text to vectors |
| [TIER-2-06](TIER-2-06-Vector-Databases.md) | Store and search vectors |
| [TIER-2-07](TIER-2-07-RAG-From-First-Principles.md) | Give LLMs your data |
| [TIER-2-08](TIER-2-08-Building-Your-First-RAG-App.md) | Build a working app |

---

## Quick Setup

### Install LangChain

```bash
pip install langchain langchain-openai langchain-community
```

### Your First LangChain Program

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", api_key="your-key")
response = llm.invoke("What is AI?")
print(response.content)
```

**That's it!** Much cleaner than raw OpenAI API calls.

---

## Self-Check

Can you answer:

- [ ] "What problem does LangChain solve?" (Reduces boilerplate for LLM apps)
- [ ] "What are the main components?" (Models, Prompts, Chains, Memory, Retrievers, etc.)
- [ ] "What's a Runnable?" (Standard interface for all LangChain objects)
- [ ] "How do you compose operations?" (Using pipe | operator)
- [ ] "Why is LangChain useful?" (Speed, flexibility, community, production-ready)

Ready for **[TIER-2-02-Models-and-LLM-Invocation.md](TIER-2-02-Models-and-LLM-Invocation.md)** →

Next: How to call LLMs through LangChain.
