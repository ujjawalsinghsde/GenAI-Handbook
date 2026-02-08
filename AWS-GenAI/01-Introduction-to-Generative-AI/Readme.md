# Introduction to Generative AI

Generative AI models create new content—text, code, images, audio, and video—by learning patterns from large datasets. This document summarizes AWS services, common architectures, and practical steps for building production systems.

## What Generative AI Produces

- Text: summaries, explanations, conversation
- Code: functions, tests, automation scripts
- Images: illustrations and style-based generation
- Audio & video: transcripts, synthesis, and multimodal outputs
- Structured data: JSON, SQL, and typed outputs

## Key AWS Services for GenAI

- **Amazon Bedrock**: Managed access to foundation models and Bedrock Knowledge Bases
- **Amazon Q**: Assistant experiences and developer productivity tools
- **Amazon SageMaker**: Model training, fine-tuning, and deployment
- **Amazon Kendra / OpenSearch**: Enterprise search and vector indexing
- **Supporting services**: S3, Lambda, API Gateway, DynamoDB for storage and orchestration

## Building a GenAI Application on AWS (High Level)

1. Select models appropriate for your task (reasoning, generation, multimodal).  
2. Ingest and store documents in S3; apply text chunking and metadata.  
3. Create embeddings and store them in a vector store (OpenSearch, PGVector, Pinecone, FAISS).  
4. Build a retriever and combine retrieved context with prompts for the model.  
5. Add agents or tool calling if the workflow requires actions (APIs, Lambdas).  
6. Deploy via API Gateway, Lambda, or containerized endpoints; monitor and iterate.

## Production Considerations

- **Security & Governance**: enforce access controls, sanitize inputs, and audit logs.  
- **Cost Management**: track token usage, set budgets, and use smaller models for high-volume tasks.  
- **Reliability**: implement retries, timeouts, and fallback models.  
- **Observability**: log prompts, responses, retrieval sources, and tool calls for debugging and compliance.  
- **Quality Control**: incorporate evaluation metrics for retrieval and final-answer accuracy.

---

This file focuses on practical design decisions; detailed examples and code are contained in module-specific READMEs.

### Deployment

Common deployment options: Bedrock, Lambda, API Gateway.

### Monitoring & Feedback

Instrument systems to improve performance, reduce cost, and ensure reliability.

---

## Key Applications of Generative Models

### Text-based applications

- Chatbots
- Summarization
- Report generation
- Document creation

### Code applications

- Code generation
- Debugging
- Refactoring
- Unit tests

### Creative applications

- Image generation
- Video generation
- Music generation

### Enterprise applications

- Knowledge assistants
- Customer support
- Content automation

### Data applications

- Data labeling
- Synthetic data creation
- Feature generation

---

## Segmentation & Tokenization (Classical NLP Techniques)

Before LLMs, NLP used simpler methods that are still useful for understanding and preprocessing text.

---

### Tokenization

Tokenization splits a sentence into smaller units (tokens).

Example:

```
"Generative AI is powerful" →
["Gener", "ative", "AI", "is", "power", "ful"]
```

Modern LLMs typically use BPE (Byte Pair Encoding) or SentencePiece.

---

### TF-IDF

TF-IDF measures a word's importance within a document corpus:

- TF (Term Frequency): how often the term appears
- IDF (Inverse Document Frequency): how rare the term is

Common uses: search engines and keyword extraction.

---

### Word2Vec

Word2Vec learns word embeddings that capture semantic relationships (e.g., King - Man + Woman = Queen). It was foundational to modern embedding techniques used with LLMs.

---

## Final Summary

Generative AI enables machines to create human-like content and power next-generation applications. AWS provides a comprehensive ecosystem — Bedrock (ready LLMs), SageMaker (custom training), Amazon Q (assistant tooling), Kendra (search), and infrastructure to deploy scalable GenAI systems.

Classical NLP techniques (tokenization, TF-IDF, Word2Vec) evolved into transformer-based LLMs; understanding these foundations remains valuable.

---
