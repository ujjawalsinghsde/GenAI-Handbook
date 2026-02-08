# AWS GenAI Syllabus

This syllabus outlines topics for designing, building, and operating generative AI solutions on AWS. Content focuses on practical, production-grade considerations for model selection, RAG, vector databases, agents, and secure deployments.

## 1. Introduction to Generative AI

- Overview of generative models and modalities (text, image, audio, video, code)
- Key AWS services for GenAI
- Typical project lifecycle and common architectures

## 2. Introduction to Large Language Models (LLMs)

- Transformer architecture and attention
- Typical evaluation metrics and benchmarks
- Trade-offs: model size, latency, cost, and safety

## 3. Amazon Foundational Models (Amazon Nova)

- Overview of Nova model family on Bedrock
- Multimodal capabilities and function-calling support

## 4. Amazon Bedrock

- Managed foundation model service: model choice, customization, secure inference
- Bedrock Knowledge Bases and RAG integrations
- Operational concerns: latency, cost optimization, monitoring, and guardrails

## 5. Prompt Engineering (with Bedrock)

- Prompt templates, few/zero-shot techniques, and output formatting
- Prompt versioning, testing, and injection mitigations

## 6. LangChain and Orchestration

- Using LangChain for chains, agents, and structured output
- Integration patterns with Bedrock and vector stores

## 7. Retrieval-Augmented Generation (RAG)

- RAG pipeline: ingestion, chunking, embeddings, vector store, retriever
- Design patterns for accuracy and traceability

## 8. Vector Databases and Knowledge Stores

- Vector DB options (OpenSearch, PGVector, Pinecone, FAISS)
- Metadata design, indexing, and versioning

## 9. Agentic Workflows & Autonomous Systems

- Agent design, tool binding, execution safety, and observability

## 10. Additional AWS GenAI Services

- Amazon Q, Amazon QuickSight generative features, SageMaker for custom models

---

## Note on Production Readiness

When using this syllabus for workshops or documentation, emphasize production topics: security, observability, cost management, data governance, and compliance. Each module should include a short runbook with deployment and monitoring recommendations.
