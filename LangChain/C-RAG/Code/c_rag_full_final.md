# Full Corrective RAG (C-RAG) with Ambiguous Merge + Query Rewrite + Web Fallback

This README documents the most complete iteration of the Corrective RAG
architecture.

This version includes:

• Internal vector retrieval\
• Per-document LLM-based scoring\
• Threshold-based classification (CORRECT / INCORRECT / AMBIGUOUS)\
• Query rewriting for improved web search precision\
• Tavily web search fallback\
• Merged internal + web knowledge for ambiguous cases\
• Sentence-level knowledge refinement\
• Constrained final answer generation

This represents a production-style, graph-based Corrective RAG system.

------------------------------------------------------------------------

# 1. Execution Flow

User Question\
↓\
Retrieve Internal Documents\
↓\
Evaluate Each Document (Score 0--1)\
↓\
Routing Decision\
├── CORRECT → Refine (Internal Only) → Generate\
├── INCORRECT → Rewrite → Web Search → Refine (Web Only) → Generate\
└── AMBIGUOUS → Rewrite → Web Search → Refine (Internal + Web) →
Generate

------------------------------------------------------------------------

# 2. Threshold Configuration

UPPER_TH = 0.7\
LOWER_TH = 0.3

Rules:

• Any score \> 0.7 → CORRECT\
• All scores \< 0.3 → INCORRECT\
• Otherwise → AMBIGUOUS

------------------------------------------------------------------------

# 3. Full Implementation Code

``` python
from typing import List, TypedDict
from pydantic import BaseModel
import re

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

# -----------------------------
# Data + Index
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

for d in chunks:
    d.page_content = d.page_content.encode("utf-8", "ignore").decode("utf-8", "ignore")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = FAISS.from_documents(chunks, embeddings)

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

UPPER_TH = 0.7
LOWER_TH = 0.3

# -----------------------------
# State
# -----------------------------
class State(TypedDict):
    question: str
    docs: List[Document]
    good_docs: List[Document]

    verdict: str
    reason: str

    strips: List[str]
    kept_strips: List[str]
    refined_context: str

    web_query: str
    web_docs: List[Document]

    answer: str

# -----------------------------
# Retrieval
# -----------------------------
def retrieve_node(state: State) -> State:
    return {"docs": retriever.invoke(state["question"])}

# -----------------------------
# Document Evaluation
# -----------------------------
class DocEvalScore(BaseModel):
    score: float
    reason: str

doc_eval_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Return relevance score in [0,1] and short reason. JSON only."),
        ("human", "Question: {question}\n\nChunk:\n{chunk}"),
    ]
)

doc_eval_chain = doc_eval_prompt | llm.with_structured_output(DocEvalScore)

def eval_each_doc_node(state: State) -> State:

    scores = []
    good_docs = []

    for d in state["docs"]:
        out = doc_eval_chain.invoke({
            "question": state["question"],
            "chunk": d.page_content
        })

        scores.append(out.score)

        if out.score > LOWER_TH:
            good_docs.append(d)

    if any(s > UPPER_TH for s in scores):
        return {"good_docs": good_docs, "verdict": "CORRECT", "reason": "High confidence retrieval."}

    if len(scores) > 0 and all(s < LOWER_TH for s in scores):
        return {"good_docs": [], "verdict": "INCORRECT", "reason": "Low relevance retrieval."}

    return {"good_docs": good_docs, "verdict": "AMBIGUOUS", "reason": "Mixed relevance signals."}

# -----------------------------
# Query Rewrite
# -----------------------------
class WebQuery(BaseModel):
    query: str

rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Rewrite into keyword-style web query (6–14 words). "
            "Add recency constraint if implied. Return JSON with key: query"
        ),
        ("human", "Question: {question}"),
    ]
)

rewrite_chain = rewrite_prompt | llm.with_structured_output(WebQuery)

def rewrite_query_node(state: State) -> State:
    out = rewrite_chain.invoke({"question": state["question"]})
    return {"web_query": out.query}

# -----------------------------
# Web Search
# -----------------------------
tavily = TavilySearchResults(max_results=5)

def web_search_node(state: State) -> State:
    query = state.get("web_query") or state["question"]
    results = tavily.invoke({"query": query})

    web_docs = []
    for r in results or []:
        text = f"TITLE: {r.get('title','')}\nURL: {r.get('url','')}\nCONTENT:\n{r.get('content') or r.get('snippet','')}"
        web_docs.append(Document(page_content=text))

    return {"web_docs": web_docs}

# -----------------------------
# Sentence-Level Refinement
# -----------------------------
def decompose_to_sentences(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if len(s.strip()) > 20]

class KeepOrDrop(BaseModel):
    keep: bool

filter_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Return keep=true only if sentence directly helps answer question. JSON only."),
        ("human", "Question: {question}\n\nSentence:\n{sentence}"),
    ]
)

filter_chain = filter_prompt | llm.with_structured_output(KeepOrDrop)

def refine(state: State) -> State:

    if state["verdict"] == "CORRECT":
        docs_to_use = state["good_docs"]
    elif state["verdict"] == "INCORRECT":
        docs_to_use = state["web_docs"]
    else:
        docs_to_use = state["good_docs"] + state["web_docs"]

    context = "\n\n".join(d.page_content for d in docs_to_use)

    strips = decompose_to_sentences(context)

    kept = []
    for s in strips:
        if filter_chain.invoke({
            "question": state["question"],
            "sentence": s
        }).keep:
            kept.append(s)

    return {"refined_context": "\n".join(kept).strip()}

# -----------------------------
# Generate
# -----------------------------
answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Answer ONLY using provided context. If insufficient say: 'I don't know.'"),
        ("human", "Question: {question}\n\nContext:\n{context}"),
    ]
)

def generate(state: State) -> State:
    out = (answer_prompt | llm).invoke({
        "question": state["question"],
        "context": state["refined_context"]
    })
    return {"answer": out.content}

# -----------------------------
# Routing
# -----------------------------
def route_after_eval(state: State) -> str:
    if state["verdict"] == "CORRECT":
        return "refine"
    else:
        return "rewrite_query"

# -----------------------------
# Graph
# -----------------------------
g = StateGraph(State)

g.add_node("retrieve", retrieve_node)
g.add_node("eval_each_doc", eval_each_doc_node)
g.add_node("rewrite_query", rewrite_query_node)
g.add_node("web_search", web_search_node)
g.add_node("refine", refine)
g.add_node("generate", generate)

g.add_edge(START, "retrieve")
g.add_edge("retrieve", "eval_each_doc")

g.add_conditional_edges(
    "eval_each_doc",
    route_after_eval,
    {
        "refine": "refine",
        "rewrite_query": "rewrite_query",
    },
)

g.add_edge("rewrite_query", "web_search")
g.add_edge("web_search", "refine")
g.add_edge("refine", "generate")

g.add_edge("generate", END)

app = g.compile()
```

------------------------------------------------------------------------

# 4. What This Version Achieves

• Handles CORRECT retrieval safely\
• Falls back to web for INCORRECT retrieval\
• Merges internal + external knowledge for AMBIGUOUS cases\
• Rewrites queries for better web precision\
• Filters context at sentence level\
• Generates constrained answers

This is a full production-style Corrective RAG system.

------------------------------------------------------------------------

# 5. Required Environment Variables

OPENAI_API_KEY=your_key\
TAVILY_API_KEY=your_key

------------------------------------------------------------------------

# 6. Summary

This implementation completes the full evolution:

Baseline RAG\
→ Refinement\
→ Retrieval Evaluation\
→ Web Fallback\
→ Query Rewrite\
→ Ambiguous Merge

You now have a complete, graph-based, safety-aware Corrective RAG
architecture.
