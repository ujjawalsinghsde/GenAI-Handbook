# Retrieval Refinement RAG using LangGraph (Sentence-Level Filtering)

This README documents an advanced Retrieval-Augmented Generation (RAG)
pipeline that introduces **sentence-level knowledge refinement** before
answer generation.

Unlike baseline RAG, this implementation:

• Decomposes retrieved documents into sentence strips\
• Uses an LLM as a strict relevance judge\
• Keeps only directly relevant sentences\
• Reconstructs a refined context\
• Generates the final answer from filtered knowledge

This improves precision and reduces noisy context.

------------------------------------------------------------------------

# 1. Overview of the Architecture

Pipeline:

User Question\
↓\
Retrieve Top-K Documents (FAISS)\
↓\
Decompose into Sentences\
↓\
LLM-Based Sentence Filtering\
↓\
Recompose Refined Context\
↓\
Generate Final Answer

------------------------------------------------------------------------

# 2. Full Implementation Code

``` python
from typing import List, TypedDict
import re

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Load and Prepare Documents
# -----------------------------
docs = (
    PyPDFLoader("./documents/book1.pdf").load()
    + PyPDFLoader("./documents/book2.pdf").load()
    + PyPDFLoader("./documents/book3.pdf").load()
)

chunks = RecursiveCharacterTextSplitter(
    chunk_size=900,
    chunk_overlap=150
).split_documents(docs)

# Clean extracted PDF text
for d in chunks:
    d.page_content = d.page_content.encode("utf-8", "ignore").decode("utf-8", "ignore")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = FAISS.from_documents(chunks, embeddings)

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# -----------------------------
# State Schema
# -----------------------------
class State(TypedDict):
    question: str
    docs: List[Document]

    strips: List[str]
    kept_strips: List[str]
    refined_context: str

    answer: str

# -----------------------------
# Retrieval Node
# -----------------------------
def retrieve(state: State) -> State:
    q = state["question"]
    return {"docs": retriever.invoke(q)}

# -----------------------------
# Sentence Decomposition
# -----------------------------
def decompose_to_sentences(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]

# -----------------------------
# LLM-Based Sentence Filter
# -----------------------------
class KeepOrDrop(BaseModel):
    keep: bool

filter_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a strict relevance filter. "
            "Return keep=true only if the sentence directly helps answer the question. "
            "Use ONLY the sentence. Output JSON only.",
        ),
        ("human", "Question: {question}\n\nSentence:\n{sentence}"),
    ]
)

filter_chain = filter_prompt | llm.with_structured_output(KeepOrDrop)

# -----------------------------
# Refinement Node
# -----------------------------
def refine(state: State) -> State:

    q = state["question"]

    # Combine retrieved docs
    context = "\n\n".join(d.page_content for d in state["docs"]).strip()

    # 1) Decompose
    strips = decompose_to_sentences(context)

    # 2) Filter
    kept: List[str] = []
    for s in strips:
        if filter_chain.invoke({"question": q, "sentence": s}).keep:
            kept.append(s)

    # 3) Recompose
    refined_context = "\n".join(kept).strip()

    return {
        "strips": strips,
        "kept_strips": kept,
        "refined_context": refined_context,
    }

# -----------------------------
# Answer Generation
# -----------------------------
answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful ML tutor. "
            "Answer ONLY using the provided refined bullets. "
            "If the bullets are empty or insufficient, say: "
            "'I don't know based on the provided books.'",
        ),
        ("human", "Question: {question}\n\nRefined context:\n{refined_context}"),
    ]
)

def generate(state: State) -> State:
    out = (answer_prompt | llm).invoke({
        "question": state["question"],
        "refined_context": state["refined_context"]
    })
    return {"answer": out.content}

# -----------------------------
# Build LangGraph Workflow
# -----------------------------
g = StateGraph(State)

g.add_node("retrieve", retrieve)
g.add_node("refine", refine)
g.add_node("generate", generate)

g.add_edge(START, "retrieve")
g.add_edge("retrieve", "refine")
g.add_edge("refine", "generate")
g.add_edge("generate", END)

app = g.compile()

# -----------------------------
# Run Example
# -----------------------------
res = app.invoke({
    "question": "Explain the bias–variance tradeoff",
    "docs": [],
    "strips": [],
    "kept_strips": [],
    "refined_context": "",
    "answer": ""
})

print(res["answer"])
```

------------------------------------------------------------------------

# 3. What Makes This Different from Basic RAG

Baseline RAG: Retrieve → Generate

This Version: Retrieve → Decompose → Filter → Recompose → Generate

Key Improvement: The LLM only sees refined, relevant knowledge instead
of full noisy documents.

------------------------------------------------------------------------

# 4. Why Sentence-Level Filtering Helps

• Removes irrelevant explanations\
• Reduces token usage\
• Improves factual precision\
• Reduces hallucination risk\
• Creates structured internal knowledge

------------------------------------------------------------------------

# 5. Requirements

``` bash
pip install langchain
pip install langchain-community
pip install langchain-openai
pip install langgraph
pip install faiss-cpu
pip install python-dotenv
```

Set environment variable:

``` bash
OPENAI_API_KEY=your_api_key
```

------------------------------------------------------------------------

# 6. Summary

This implementation represents the **Knowledge Refinement stage** of
Corrective RAG.

It introduces:

• Sentence-level decomposition\
• LLM-based strict filtering\
• Structured refined context\
• Clean LangGraph orchestration

This is a critical intermediate step before implementing full Retrieval
Evaluation and Web Fallback in a complete C-RAG system.
