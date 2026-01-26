# 📘 **1. Amazon Textract – Text Extraction Architecture**

```
          +-----------------------------+
          |        Input Sources        |
          |  PDFs | Images | Scanned Docs|
          +-----------------------------+
                         |
                         v
                +-------------------+
                |   Amazon Textract |
                |  OCR + Tables +   |
                |  Forms Extraction |
                +-------------------+
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
 +--------------+  +--------------+  +--------------+
 | Extracted    |  | Key-Value    |  | Table Cells  |
 | Text         |  | Pairs        |  | Structured   |
 | (streams)    |  |              |  | Data         |
 +--------------+  +--------------+  +--------------+
                         |
                         v
                 +----------------+
                 | Output Storage |
                 | S3 / DynamoDB  |
                 +----------------+
```

---

# 📘 **2. Amazon Rekognition – Image Text & Image Analysis Architecture**

```
           +---------------------+
           |      Images         |
           +---------------------+
                    |
                    v
         +-------------------------+
         | Amazon Rekognition      |
         | Text Detection / Labels |
         +-------------------------+
                    |
     +--------------+---------------+
     |                              |
     v                              v
+-----------+                +----------------+
| Detected  |                | Detected Labels|
| Text      |                | (Objects, scenes)
+-----------+                +----------------+
                    |
                    v
          +-----------------------+
          | Analytics / Pipeline  |
          | Lambda / S3 / RDS     |
          +-----------------------+
```

---

# 📘 **3. Amazon Q (Developer Assistant + CodeWhisperer)**

```
           +---------------------------+
           | Developer IDE (VSCode etc)|
           +---------------------------+
                         |
                         v
           +---------------------------+
           |       Amazon Q            |
           | Code Suggest + Fix + Docs |
           +---------------------------+
                         |
        +----------------+----------------+
        |                                 |
        v                                 v
+------------------+              +---------------------+
| Code Generation  |              | AWS Cloud Guidance  |
| Snippets/Functions|             | Architecture help   |
+------------------+              +---------------------+
                         |
                         v
                +-----------------------+
                | Commit / Deploy       |
                | GitHub / CodePipeline |
                +-----------------------+
```

---

# 📘 **4. Amazon Q Business – Enterprise Search & Chat**

```
          +----------------------------------+
          |    Company Data Sources          |
          | S3 | SharePoint | GDrive | Jira  |
          +----------------------------------+
                         |
                         v
            +-----------------------------+
            |  Amazon Q Business Indexer  |
            | (Crawling + Chunking +      |
            | Embeddings + Syncing)       |
            +-----------------------------+
                         |
               +---------+--------+
               | Vector Index     |
               | (Search Engine)  |
               +---------+--------+
                         |
                         v
           +-----------------------------+
           |  Amazon Q Business Model    |
           | (LLM + RAG + Reasoning)     |
           +-----------------------------+
                         |
                         v
              +----------------------+
              | Web/App Chatbot UI  |
              +----------------------+
```

---

# 📘 **5. Amazon QuickSight – Generative BI Architecture**

```
          +------------------------------+
          |   Data Sources (S3, RDS,     |
          |   Redshift, Athena, API)     |
          +------------------------------+
                     |
                     v
            +--------------------------+
            | QuickSight SPICE Engine |
            | (Caching + Optimization)|
            +--------------------------+
                     |
                     v
       +------------------------------------+
       | QuickSight Generative Capabilities |
       | Ask Q (NLQ)  | Gen Insights | ML   |
       +------------------------------------+
                     |
                     v
           +-----------------------------+
           | Dashboards, Charts, Stories |
           +-----------------------------+
```

---

# 📘 **6. AWS App Studio – AI Assisted App Builder**

```
         +-----------------------+
         | User gives requirement|
         | (Natural language)    |
         +-----------------------+
                     |
                     v
     +--------------------------------------+
     | AWS App Studio (AI Understanding)    |
     | UI Generation | Backend Logic | Data |
     +--------------------------------------+
                     |
        +------------+-------------+
        |                          |
        v                          v
+------------------+      +---------------------+
| Frontend Builder |      | Backend Services    |
| React UI         |      | Lambda / API GW     |
+------------------+      +---------------------+
                     |
                     v
           +------------------------------+
           | Auto Deployment to AWS Cloud |
           +------------------------------+
```

---

# 📘 **7. Bedrock Model Families (Nova, Claude, Llama, Mistral, Titan)**

```
          +------------------------------------+
          |       Amazon Bedrock Platform      |
          +------------------------------------+
               |         |         |        |
               v         v         v        v
      +-----------+ +-----------+ +-------+ +----------+
      | Amazon    | | Anthropic | | Meta  | | Mistral  |
      | Nova/Titan| | Claude    | | Llama | | Models   |
      +-----------+ +-----------+ +-------+ +----------+
               \         |         / 
                \        |        /
                 \       |       /
                  v      v      v
                 +---------------------+
                 |  Bedrock Inference  |
                 +---------------------+
                         |
                         v
                   Your Application
```

---

# 📘 **8. Bedrock Prompt Flows – Workflow Automation**

```
       +-----------------------+
       |   User Prompt Input   |
       +-----------------------+
                   |
                   v
      +-------------------------------+
      |    Prompt Flow Orchestrator   |
      |  (Workflow builder in Bedrock)|
      +-------------------------------+
        |       |           |       |
        v       v           v       v
   +---------+ +---------+ +------+,-------+
   | Prompts | | RAG KB  | | Tools | Agent |
   +---------+ +---------+ +---------+-----+
                   \       |       /
                    \      |      /
                     v     v     v
               +---------------------+
               |   Bedrock Model     |
               | (Nova / Claude etc) |
               +---------------------+
                           |
                           v
                 +----------------+
                 | Final Response |
                 +----------------+
```

---

# 📘 **9. Security & Compliance Essentials Architecture**

```
                +----------------------------+
                |   AWS Security Framework   |
                +----------------------------+
                       |     |      | 
                       v     v      v
        +----------------+  +----------------+
        | IAM Controls   |  | VPC Isolation  |
        +----------------+  +----------------+
                       |
                       v
            +---------------------------+
            | Encryption (KMS/TLS)      |
            +---------------------------+
                       |
                       v
            +---------------------------+
            | Guardrails (Content Safety)|
            +---------------------------+
                       |
                       v
            +----------------------------+
            | Monitoring (CloudWatch, XRay)|
            +----------------------------+
                       |
                       v
               +------------------+
               | Secure GenAI App |
               +------------------+
```
