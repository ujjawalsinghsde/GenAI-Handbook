# Corrective RAG with Web Search Fallback (Full Iteration with Tavily Integration)

This README documents an extended Corrective RAG (C-RAG) pipeline that
integrates:

• Retrieval Evaluation\
• Threshold-Based Routing\
• Web Search Fallback (Tavily)\
• Sentence-Level Refinement\
• Unified Generation Logic

This version represents a near-complete Corrective RAG system.

------------------------------------------------------------------------

# 1. Architecture Overview

Pipeline Flow:

User Question\
↓\
Retrieve Top-K Documents (Vector DB)\
↓\
Evaluate Each Document (LLM Scoring)\
↓\
Routing Based on Thresholds\
├── CORRECT → Refine Internal Docs → Generate\
├── INCORRECT → Web Search → Refine Web Docs → Generate\
└── AMBIGUOUS → Ambiguous Handler\
↓\
Return Final Answer

------------------------------------------------------------------------

# 2. Key Additions in This Version

Compared to the previous evaluator-only version, this iteration adds:

• Tavily web search integration\
• web_docs added to state\
• Unified refine() handling both internal and web documents\
• Conditional edge routing to web_search node

This completes the fallback mechanism of C-RAG.

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

# Web Search Integration
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

# -----------------------------
# Document Preparation
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
# State Definition
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

    web_docs: List[Document]

    answer: str

# -----------------------------
# Retrieval Node
# -----------------------------
def retrieve_node(state: State) -> State:
    return {"docs": retriever.invoke(state["question"])}

# -----------------------------
# Retrieval Evaluation
# -----------------------------
class DocEvalScore(BaseModel):
    score: float
    reason: str

doc_eval_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Return a relevance score in [0.0, 1.0] and a short reason.
"
            "Be conservative with high scores.
"
            "Output JSON only.",
        ),
        ("human", "Question: {question}

Chunk:
{chunk}"),
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
        return {
            "good_docs": good_docs,
            "verdict": "CORRECT",
            "reason": f"At least one chunk scored > {UPPER_TH}.",
        }

    if len(scores) > 0 and all(s < LOWER_TH for s in scores):
        return {
            "good_docs": [],
            "verdict": "INCORRECT",
            "reason": f"All chunks scored < {LOWER_TH}.",
        }

    return {
        "good_docs": good_docs,
        "verdict": "AMBIGUOUS",
        "reason": "Mixed relevance signals.",
    }

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
        ("system", "Return keep=true only if sentence directly answers the question. JSON only."),
        ("human", "Question: {question}\n\nSentence:\n{sentence}"),
    ]
)

filter_chain = filter_prompt | llm.with_structured_output(KeepOrDrop)

def refine(state: State) -> State:

    if state["verdict"] == "CORRECT":
        context = "\n\n".join(d.page_content for d in state["good_docs"])
    else:
        context = "\n\n".join(d.page_content for d in state["web_docs"])

    strips = decompose_to_sentences(context)

    kept = []
    for s in strips:
        if filter_chain.invoke({
            "question": state["question"],
            "sentence": s
        }).keep:
            kept.append(s)

    refined_context = "\n".join(kept).strip()

    return {
        "strips": strips,
        "kept_strips": kept,
        "refined_context": refined_context,
    }

# -----------------------------
# Web Search Node
# -----------------------------
tavily = TavilySearchResults(max_results=5)

def web_search_node(state: State) -> State:

    results = tavily.invoke({"query": state["question"]})

    web_docs = []
    for r in results or []:
        text = f"TITLE: {r.get('title','')}\nURL: {r.get('url','')}\nCONTENT:\n{r.get('content') or r.get('snippet','')}"
        web_docs.append(Document(page_content=text))

    return {"web_docs": web_docs}

# -----------------------------
# Generation Node
# -----------------------------
answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Answer ONLY using provided context. If insufficient, say: 'I don't know.'"),
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
# Routing Logic
# -----------------------------
def ambiguous_node(state: State) -> State:
    return {"answer": f"Ambiguous: {state['reason']}"}

def route_after_eval(state: State) -> str:
    if state["verdict"] == "CORRECT":
        return "refine"
    elif state["verdict"] == "INCORRECT":
        return "web_search"
    else:
        return "ambiguous"

# -----------------------------
# Graph Construction
# -----------------------------
g = StateGraph(State)

g.add_node("retrieve", retrieve_node)
g.add_node("eval_each_doc", eval_each_doc_node)
g.add_node("web_search", web_search_node)
g.add_node("refine", refine)
g.add_node("generate", generate)
g.add_node("ambiguous", ambiguous_node)

g.add_edge(START, "retrieve")
g.add_edge("retrieve", "eval_each_doc")

g.add_conditional_edges(
    "eval_each_doc",
    route_after_eval,
    {
        "refine": "refine",
        "web_search": "web_search",
        "ambiguous": "ambiguous",
    },
)

g.add_edge("web_search", "refine")
g.add_edge("refine", "generate")

g.add_edge("generate", END)
g.add_edge("ambiguous", END)

app = g.compile()
```

------------------------------------------------------------------------

# 4. What This Version Achieves

• Adds external knowledge fallback\
• Handles missing internal knowledge\
• Maintains structured state transitions\
• Reuses refinement logic for both internal and web data\
• Implements true corrective routing

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

Set environment variables:

OPENAI_API_KEY=your_key\
TAVILY_API_KEY=your_key

------------------------------------------------------------------------

# 6. Summary

This implementation completes the Web Search fallback stage of
Corrective RAG.

The system now:

• Validates retrieval quality\
• Routes conditionally\
• Falls back to external web search\
• Refines context before generation\
• Produces safer, more reliable outputs

This is a full working prototype of a Web-Integrated Corrective RAG
architecture.
