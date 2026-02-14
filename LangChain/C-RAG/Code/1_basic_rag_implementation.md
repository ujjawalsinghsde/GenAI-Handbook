# Basic RAG Implementation using LangGraph

This README documents a clean implementation of a Basic
Retrieval-Augmented Generation (RAG) system using:

-   LangChain
-   FAISS (Vector Store)
-   OpenAI Embeddings
-   ChatOpenAI (LLM)
-   LangGraph (Workflow Orchestration)

This version does NOT include Corrective RAG logic.\
It represents a standard linear RAG pipeline: Retrieve → Generate.

------------------------------------------------------------------------

# 1. Overview

This implementation performs:

1.  Load PDF documents
2.  Split into chunks
3.  Clean extracted text
4.  Create embeddings
5.  Store in FAISS vector store
6.  Retrieve top-k documents
7.  Generate answer using context
8.  Orchestrate workflow using LangGraph

------------------------------------------------------------------------

# 2. Full Code

``` python
from typing import List, TypedDict
import time

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

# 1) Load PDFs
docs = (
    PyPDFLoader("./documents/book1.pdf").load() +
    PyPDFLoader("./documents/book2.pdf").load() +
    PyPDFLoader("./documents/book3.pdf").load()
)

# 2) Chunk Documents
chunks = RecursiveCharacterTextSplitter(
    chunk_size=900,
    chunk_overlap=150
).split_documents(docs)

# 3) Clean text to avoid UnicodeEncodeError from PDF extraction
for d in chunks:
    d.page_content = d.page_content.encode("utf-8", "ignore").decode("utf-8", "ignore")

# 4) Create Vector Store
embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
vector_store = FAISS.from_documents(chunks, embeddings)

retriever = vector_store.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 4}
)

# 5) Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 6) Define State Schema
class State(TypedDict):
    question: str
    docs: List[Document]
    answer: str

# 7) Retrieval Node
def retrieve(state):
    q = state["question"]
    return {"docs": retriever.invoke(q)}

# 8) Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Answer only from the context. If not in context, say you don't know."),
        ("human", "Question: {question}\n\nContext:\n{context}"),
    ]
)

# 9) Generation Node
def generate(state):
    context = "\n\n".join(d.page_content for d in state["docs"])
    out = (prompt | llm).invoke({
        "question": state["question"],
        "context": context
    })
    return {"answer": out.content}

# 10) Build LangGraph Workflow
g = StateGraph(State)

g.add_node("retrieve", retrieve)
g.add_node("generate", generate)

g.add_edge(START, "retrieve")
g.add_edge("retrieve", "generate")
g.add_edge("generate", END)

app = g.compile()

# 11) Run Query
res = app.invoke({
    "question": "What is a transformer in deep learning?",
    "docs": [],
    "answer": ""
})

print(res["answer"])
```

------------------------------------------------------------------------

# 3. Architecture Flow

User Question\
↓\
Retrieve top-4 documents from FAISS\
↓\
Inject context into prompt\
↓\
Generate answer using LLM\
↓\
Return final response

------------------------------------------------------------------------

# 4. Key Design Decisions

• Chunk Size: 900 with 150 overlap for semantic continuity\
• Embedding Model: text-embedding-3-large\
• LLM: gpt-4o-mini (deterministic with temperature=0)\
• Vector Store: FAISS for fast similarity search\
• Workflow Engine: LangGraph for structured state management

------------------------------------------------------------------------

# 5. Important Notes

1.  This is a linear RAG pipeline.
2.  No retrieval validation is performed.
3.  If incorrect documents are retrieved, hallucination risk remains.
4.  Suitable as a baseline before implementing Corrective RAG.

------------------------------------------------------------------------

# 6. Requirements

Install dependencies:

``` bash
pip install langchain
pip install langchain-community
pip install langchain-openai
pip install langgraph
pip install faiss-cpu
pip install python-dotenv
```

Ensure environment variables are configured:

``` bash
OPENAI_API_KEY=your_api_key
```
