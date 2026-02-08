# Other GenAI Services with AWS

AWS provides an ecosystem of generative AI tools beyond Bedrock and Nova.
These services support text extraction, document analysis, BI, code generation, and application scaffolding.

Overview of topics.

---

## Text Extraction from Documents and Images

AWS offers multiple services to extract text from:

- PDFs
- Images
- Scanned documents
- IDs
- Forms
- Tables

---

### Amazon Textract — Text Extraction Service

Amazon Textract extracts:

- Printed text
- Handwriting
- Tables
- Form fields and key-value pairs

Example: a bank statement ingestion returns structured table rows, amounts, names, and dates.

Why use Textract:

- Reliable PDF scanning
- Preserves table structure
- Extracts form fields accurately

---

### Amazon Rekognition — Image Text Extraction

Amazon Rekognition detects text and image labels. Typical uses:

- Photos
- IDs and documents
- Signboards and invoices

---

### Bedrock models for text extraction

Amazon Nova and other multimodal models can extract text, interpret diagrams, and analyze document structure.

Example: image of a bill → model returns itemized descriptions.

---

## Amazon Q (CodeWhisperer features)

Amazon Q is a general-purpose AI assistant for developers, cloud engineers, business users, and support teams.

It integrates with the AWS Console, IDEs, and documentation.

---

### CodeWhisperer features in Amazon Q

Key capabilities:

#### Code generation

Generate code from prompts (for example, an API endpoint in Python using Lambda).

#### Code explanations

Explain code intent and usage.

#### Bug fixing and suggestions

Propose fixes and improvements.

#### Security scanning

Detect common vulnerabilities.

#### Code modernization

Assist with upgrades and refactoring.

---

## Amazon Q Business

Amazon Q Business is an enterprise chatbot that indexes company data and answers domain-specific queries.

Capabilities:

- Enterprise search across documents
- Domain-specific question answering
- Summarization of emails and tickets
- Workflow automation with access controls

Data sources supported:

- SharePoint
- Google Drive
- Confluence
- Jira
- S3
- Salesforce
- GitHub
- Internal wikis

Why it is useful:

- Supports RAG-based retrieval
- Designed for enterprise security and governance
- No model fine-tuning required for common use cases

Example: summarize incidents and highlight top risks.

---


## Amazon QuickSight — Generative BI

Amazon QuickSight provides natural-language BI capabilities and generative insights.

Capabilities:

#### Natural-language queries

Create charts and metrics by asking questions in plain language (for example, sales by month).

#### Auto-generate dashboards

Generate charts, KPIs, and visuals from high-level prompts.

#### Explainable insights

Summarize trends, patterns, and anomalies.

#### Forecasting

Provide predictive insights based on historical data.

#### Narrative generation

Translate visualizations into written summaries.

---


## AWS App Studio — AI-assisted App Builder

AWS App Studio generates UI screens, backend logic, API integration, and deployment artifacts from natural-language requirements.

Capabilities:

- UI generation
- Backend scaffolding (Lambda, API Gateway)
- Database integration
- Authentication and deployment

Example: describe an employee management app and App Studio scaffolds the UI, DynamoDB table, API routes, and authentication.

Suitable for rapid prototyping and product discovery.

---


## Bedrock Model Families

Bedrock provides access to multiple model families:

### Amazon models

- Nova (Pro, Lite, Micro)
- Titan Text
- Titan Embeddings
- Titan Image

### Anthropic

- Claude 3 series (various flavors)

### Meta

- Llama 3 series

### Mistral

- Mistral 7B, Mixtral, and larger variants

### Stability AI

- SDXL and image models

### Cohere

- Command R and embedding models

---


## Bedrock Prompt Flows

Prompt Flows enable end-to-end GenAI workflows combining prompts, tools, RAG, chains, agents, function calling, and multi-step processing.

Typical workflow: `User → Prompt → RAG → Nova → Tool Call → Final Answer`.

Use cases:

- Customer support
- Knowledge assistants
- Automation
- Document processing

---


## Security and Compliance Essentials

AWS provides enterprise security features for GenAI workloads.

### Data protection

- Customer data is not used for model training by default
- Encryption in transit (TLS) and at rest (KMS)
- VPC isolation options

### IAM controls

Restrict access to Bedrock, agent tools, knowledge bases, and APIs via IAM roles.

### Guardrails

Mitigate harmful outputs and sensitive data exposure.

### Prompt injection protection

Protect models from malicious prompt overrides and enforce instruction integrity.

### Compliance

Bedrock supports common compliance standards (SOC, HIPAA, GDPR, ISO, FedRAMP).

---


## Final Summary — Other GenAI Services with AWS

| Topic | Summary |
| ----- | ------- |
| Textract | Extract text from PDFs, forms, and images |
| Amazon Q | AI assistant with CodeWhisperer features |
| Q Business | Enterprise chatbot with company-data indexing |
| QuickSight GenAI | Natural-language BI and generative insights |
| App Studio | Natural-language app scaffolding and deployment |
| Bedrock Models | Access to Nova, Claude, Llama, Mistral, Titan, etc. |
| Prompt Flows | Visual workflow builder for GenAI pipelines |
| Security | Guardrails, IAM, encryption, and compliance |

AWS provides a complete GenAI ecosystem covering text extraction, reasoning, RAG, analytics, application scaffolding, enterprise search, and security.

---
