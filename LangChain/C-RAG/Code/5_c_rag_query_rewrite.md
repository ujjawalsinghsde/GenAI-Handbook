# Corrective RAG with Query Rewriting + Web Fallback (Full Pipeline)

This README documents the most advanced iteration of the Corrective RAG
(C-RAG) system.

This version includes:

• Retrieval from internal vector database\
• LLM-based retrieval evaluation\
• Threshold-based conditional routing\
• Query rewriting for improved web search\
• Tavily web search fallback\
• Sentence-level knowledge refinement\
• Final constrained answer generation

This represents a complete end-to-end Corrective RAG architecture.

------------------------------------------------------------------------

# 1. Architecture Overview

Full Execution Flow:

User Question\
↓\
Retrieve Internal Documents\
↓\
Evaluate Each Document (LLM Scoring)\
↓\
Routing Decision\
├── CORRECT → Refine Internal Docs → Generate\
├── INCORRECT → Rewrite Query → Web Search → Refine → Generate\
└── AMBIGUOUS → Ambiguous Handler\
↓\
Return Final Answer

------------------------------------------------------------------------

# 2. Key Improvements in This Version

Compared to the previous version:

• Added `web_query` to state\
• Added query rewriting node\
• Web search now uses rewritten query\
• Cleaner separation of routing logic\
• Stronger web search precision

This version aligns closely with research-level Corrective RAG.

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
    web_query: str

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
        ("system", "Return a relevance score in [0.0, 1.0] and a short reason. JSON only."),
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
# Query Rewrite Node
# -----------------------------
class WebQuery(BaseModel):
    query: str

rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Rewrite question into keyword-style web search query.
"
            "Keep 6–14 words. Add recency constraint if implied.
"
            "Return JSON with key: query"
        ),
        ("human", "Question: {question}"),
    ]
)

rewrite_chain = rewrite_prompt | llm.with_structured_output(WebQuery)

def rewrite_query_node(state: State) -> State:
    out = rewrite_chain.invoke({"question": state["question"]})
    return {"web_query": out.query}

# -----------------------------
# Web Search Node
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
        ("system", "Return keep=true only if sentence directly answers question. JSON only."),
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
# Answer Generation
# -----------------------------
answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Answer ONLY using provided context. If insufficient say: 'I don't know.'"),
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
        return "rewrite_query"
    else:
        return "ambiguous"

# -----------------------------
# Graph Construction
# -----------------------------
g = StateGraph(State)

g.add_node("retrieve", retrieve_node)
g.add_node("eval_each_doc", eval_each_doc_node)
g.add_node("rewrite_query", rewrite_query_node)
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
        "rewrite_query": "rewrite_query",
        "ambiguous": "ambiguous",
    },
)

g.add_edge("rewrite_query", "web_search")
g.add_edge("web_search", "refine")
g.add_edge("refine", "generate")

g.add_edge("generate", END)
g.add_edge("ambiguous", END)

app = g.compile()
```

------------------------------------------------------------------------

# 4. What This Version Achieves

• Internal retrieval validation\
• Query optimization for web search\
• Reliable external fallback\
• Sentence-level knowledge refinement\
• Fully structured graph-based execution\
• Near research-grade C-RAG implementation

------------------------------------------------------------------------

# 5. Required Environment Variables

OPENAI_API_KEY=your_key\
TAVILY_API_KEY=your_key

------------------------------------------------------------------------

# 6. Summary

This implementation represents the final, complete version of Corrective
RAG in your progression.

It transforms traditional RAG into:

Retrieve → Evaluate → Route → Rewrite → Search → Refine → Generate

This is a production-aligned, safety-aware, and extensible C-RAG
architecture.
