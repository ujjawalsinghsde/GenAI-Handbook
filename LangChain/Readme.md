# LangChain Learning Notes

This repository provides a structured and comprehensive reference for understanding and implementing LangChain.  
It is organized as a progressive learning path, starting with the fundamentals and advancing toward retrieval systems, tool-calling workflows, and agent-based architectures.  
All modules are aligned with practical GenAI development and can be used as standalone study material or as part of a larger system design.

---

# Learning Roadmap (Follow in Order)

Each module includes explanations, examples, and practical guidance.

---

## 01 — Introduction to LangChain

📁 Folder: [`/01-Introduction-to-LangChain`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/01-Introduction-to-LangChain/Readme.md)

Covers the fundamentals of LangChain:

- What LangChain is and why it is used
- Core abstractions (Models, Prompts, Chains, Agents)
- How LangChain simplifies LLM application development
- High-level architecture and workflow

This is the conceptual foundation for the entire module.

---

## 02 — Models

📁 Folder: [`/02-Models`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/02-Models/Readme.md)

Learn about the different model types supported in LangChain:

- Chat models
- Completion models
- Embedding models
- Invocation patterns for each model
- Provider integration (OpenAI, Anthropic, Bedrock, etc.)

Understanding models is essential before building pipelines.

---

## 03 — Prompts

📁 Folder: [`/03-Prompts`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/03-Prompts/Readme.md)

A complete guide on writing robust prompts:

- Prompt templates
- System, user, and assistant roles
- Variables and formatting
- Style and tone instructions
- Best practices for reliability

This section improves prompt clarity and reduces ambiguity.

---

## 04 — Structured Output

📁 Folder: [`/04-Structured-Output`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/04-Structured-Output/Readme.md)

Learn how to instruct LLMs to return structured formats:

- JSON schemas
- Typed outputs
- Enforcing structure in LLM responses
- Validating and parsing structured outputs

Critical for production-grade pipelines.

---

## 05 — Output Parsers

📁 Folder: [`/05-Output-Parsers`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/05-Output-Parsers/Readme.md)

Output parsers help convert raw LLM text into usable formats:

- JSON parsing
- List extraction
- Dataclass parsing
- Handling model errors and retries

Useful when combining LLMs with downstream logic.

---

## 06 — Chains

📁 Folder: [`/06-Chains`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/06-Chains/Readme.md)

Chains allow multiple steps to be combined into a single workflow:

- Prompt → model → parser
- Retrieval chains
- Multi-step logical workflows
- Input/output orchestration

Chains are the backbone of LangChain applications.

---

## 07 — Runnable

📁 Folder: [`/07-Runnable`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/07-Runnable/Readme.md)

Learn the LangChain Expression Language (LCEL):

- Runnable sequences
- Parallel execution
- Map/reduce patterns
- Streaming outputs

Runnables are the modern execution layer under the hood.

---

## 08 — Document Loaders

📁 Folder: [`/08-Document-Loaders`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/08-Document-Loaders/Readme.md)

Load content from various data sources:

- PDFs
- Web pages
- Notion
- GitHub
- YouTube transcripts

The first stage of the RAG pipeline.

---

## 09 — Text Splitter

📁 Folder: [`/09-Text-Splitter`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/09-Text-Splitter/Readme.md)

Chunking documents before embedding:

- Recursive splitters
- Document-aware splitters
- Chunk size and overlap strategy
- Maintaining semantic flow

A key step for RAG accuracy.

---

## 10 — Vector Stores

📁 Folder: [`/10-Vector-Stores`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/10-Vector-Stores/Readme.md)

Vector stores persist embeddings and enable similarity search:

- FAISS  
- Pinecone  
- ChromaDB  
- Milvus  
- Metadata storage strategy

Acts as the retrieval database for GenAI systems.

---

## 11 — Retrievers

📁 Folder: [`/11-Retrievers`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/11-Retrievers/Readme.md)

Retrievers return relevant information using:

- Similarity search
- Max marginal relevance (MMR)
- Multi-query retrieval
- Contextual compression
- Self-query retrievers

Retrievers determine the quality of responses in RAG.

---

## 12 — RAG (Retrieval-Augmented Generation)

📁 Folder: [`/12-RAG`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/12-RAG/Readme.md)

Complete RAG workflow design:

- Chunking → embeddings → vector storage
- Retrieval strategies
- Query transformation
- Evidence-based generation
- Reducing hallucinations
- RAG evaluation and benchmarking

This module integrates everything from 01–11.

---

## 13 — YouTube Chatbot

📁 Folder: [`/13-YouTube-Chatbot`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/13-YouTube-Chatbot/Readme.md)

A hands-on project demonstrating:

- Loading and chunking YouTube transcripts
- Embedding and indexing
- Retriever pipelines
- Asking contextual questions from video content

A complete, practical RAG implementation.

---

## 14 — Tools

📁 Folder: [`/14-Tools`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/14-Tools/Readme.md)

Learn how to give LLMs capabilities:

- API calls
- Database queries
- External operations (math, search, utilities)
- Tool schema definitions

Tools allow the model to take actions beyond text generation.

---

## 15 — Tool Calling

📁 Folder: [`/15-Tool-Calling`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/15-Tool%20Calling/Readme.md)

Modern LLMs can intelligently choose tools.

Covered topics:

- Tool definitions
- Auto-selection logic
- Function-calling workflows
- Multi-tool reasoning and planning

Essential for agent development.

---

## 16 — AI Agents

📁 Folder: [`/16-AI-Agents`](https://github.com/ujjawalsinghsde/GenAI-Handbook/blob/main/LangChain/16-AI%20Agents/Readme.md)

Agents execute multi-step reasoning loops and use tools.

You will learn:

- ReAct (Reasoning + Acting)
- Tool-aware agents
- Planning and execution loops
- Memory integration
- Multi-step autonomous workflows

This is the advanced stage of LangChain development.

---

# Project Structure Overview

```
LangChain
 ├── 01-Introduction-to-LangChain
 ├── 02-Models
 ├── 03-Prompts
 ├── 04-Structured-Output
 ├── 05-Output-Parsers
 ├── 06-Chains
 ├── 07-Runnable
 ├── 08-Document-Loaders
 ├── 09-Text-Splitter
 ├── 10-Vector-Stores
 ├── 11-Retrievers
 ├── 12-RAG
 ├── 13-YouTube-Chatbot
 ├── 14-Tools
 ├── 15-Tool-Calling
 └── 16-AI-Agents
```
