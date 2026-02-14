# Retrieval Evaluator RAG with Conditional Routing (Pre-Corrective RAG Stage)

This README documents an advanced Retrieval-Augmented Generation (RAG)
pipeline that introduces:

• Per-document relevance scoring\
• Threshold-based classification (CORRECT / INCORRECT / AMBIGUOUS)\
• Conditional routing using LangGraph\
• Sentence-level refinement for high-quality context\
• Safe failure handling

This represents the core Retrieval Evaluation stage of Corrective RAG
(C-RAG).

------------------------------------------------------------------------

# 1. Architecture Overview

Pipeline Flow:

User Question\
↓\
Retrieve Top-K Documents\
↓\
Score Each Document (LLM Judge)\
↓\
Classification Based on Thresholds\
├── CORRECT → Refine → Generate\
├── INCORRECT → Fail (placeholder for Web Search)\
└── AMBIGUOUS → Ambiguous Handler\
↓\
Return Final Output

------------------------------------------------------------------------

# 2. Threshold Logic

Two thresholds control routing:

UPPER_TH = 0.7\
LOWER_TH = 0.3

Rules:

• If any document score \> 0.7 → CORRECT\
• If all document scores \< 0.3 → INCORRECT\
• Otherwise → AMBIGUOUS

This converts linear RAG into a decision-based workflow.

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
# State Schema
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

    answer: str

# -----------------------------
# Retrieval Node
# -----------------------------
def retrieve_node(state: State) -> State:
    return {"docs": retriever.invoke(state["question"])}

# -----------------------------
# Document Scoring Model
# -----------------------------
class DocEvalScore(BaseModel):
    score: float
    reason: str

doc_eval_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a strict retrieval evaluator for RAG."
            "Return a relevance score in [0.0, 1.0]."
            "Be conservative with high scores."
            "Also return a short reason."
            "Output JSON only.",
        ),
        ("human", "Question: {question}

Chunk:
{chunk}"),
    ]
)

doc_eval_chain = doc_eval_prompt | llm.with_structured_output(DocEvalScore)

# -----------------------------
# Evaluation Node
# -----------------------------
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
            "reason": f"At least one chunk scored > {UPPER_TH}."
        }

    if len(scores) > 0 and all(s < LOWER_TH for s in scores):
        return {
            "good_docs": [],
            "verdict": "INCORRECT",
            "reason": f"All chunks scored < {LOWER_TH}."
        }

    return {
        "good_docs": good_docs,
        "verdict": "AMBIGUOUS",
        "reason": "Mixed relevance signals."
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
        (
            "system",
            "Return keep=true only if the sentence directly helps answer the question."
            "Output JSON only."
        ),
        ("human", "Question: {question}

Sentence:
{sentence}"),
    ]
)

filter_chain = filter_prompt | llm.with_structured_output(KeepOrDrop)

def refine(state: State) -> State:

    context = "\n\n".join(d.page_content for d in state["good_docs"]).strip()
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
        "refined_context": refined_context
    }

# -----------------------------
# Answer Generation
# -----------------------------
answer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Answer ONLY using the provided context."
            "If context is empty, say: 'I don't know.'"
        ),
        ("human", "Question: {question}

Refined context:
{refined_context}"),
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
def fail_node(state: State) -> State:
    return {"answer": f"FAIL: {state['reason']}"}

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
# LangGraph Workflow
# -----------------------------
g = StateGraph(State)

g.add_node("retrieve", retrieve_node)
g.add_node("eval_each_doc", eval_each_doc_node)
g.add_node("refine", refine)
g.add_node("generate", generate)
g.add_node("fail", fail_node)
g.add_node("ambiguous", ambiguous_node)

g.add_edge(START, "retrieve")
g.add_edge("retrieve", "eval_each_doc")

g.add_conditional_edges(
    "eval_each_doc",
    route_after_eval,
    {
        "refine": "refine",
        "web_search": "fail",
        "ambiguous": "ambiguous",
    },
)

g.add_edge("refine", "generate")
g.add_edge("generate", END)
g.add_edge("fail", END)

app = g.compile()
```

------------------------------------------------------------------------

# 4. What This Implementation Achieves

• Introduces retrieval quality validation\
• Prevents blind trust in retrieved documents\
• Enables conditional execution paths\
• Prepares foundation for Web Search fallback\
• Moves system closer to full Corrective RAG

------------------------------------------------------------------------

# 5. Key Conceptual Upgrade Over Previous Version

Baseline RAG: Retrieve → Generate

Refinement RAG: Retrieve → Refine → Generate

This Version: Retrieve → Evaluate → Route → Refine → Generate

This is the architectural shift from linear pipelines to decision-based
graphs.

------------------------------------------------------------------------

# 6. Requirements

``` bash
pip install langchain
pip install langchain-community
pip install langchain-openai
pip install langgraph
pip install faiss-cpu
pip install python-dotenv
```

Set:

OPENAI_API_KEY=your_api_key

------------------------------------------------------------------------

# 7. Summary

This implementation represents the Retrieval Evaluation stage of
Corrective RAG.

It introduces:

• Score-based document validation\
• Threshold-driven routing\
• Structured state transitions\
• Failure-safe outputs

The next logical extension is adding a real Web Search node for the
INCORRECT and AMBIGUOUS cases to complete the full C-RAG system.
