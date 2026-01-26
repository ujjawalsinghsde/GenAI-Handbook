# 📘 **LangChain**

LangChain is a **framework** that helps developers build powerful applications using Large Language Models (LLMs).
It provides the tools, building blocks, and integrations needed to create production-ready AI apps like chatbots, agents, RAG, and automated workflows.

---

# 1️⃣ **Introduction to LangChain**

### 👉 **What is LangChain?**

LangChain is a **Python/JavaScript framework** that simplifies working with LLMs like:

* OpenAI
* Amazon Bedrock
* Anthropic
* Google Gemini
* Llama/Mistral
* Hugging Face

It helps build:

* Chatbots
* RAG systems
* Agents
* LLM-powered APIs
* Document analysis tools
* Multi-step workflows

### 👉 **Why LangChain?**

LLMs alone generate text.
LangChain helps you build **applications** around them by providing:

* Prompt templates
* Chains
* Memory
* Agents
* Runnables
* Parsers
* Tools
* Integrations
* Document loaders
* Vector stores

It organizes your app into reusable blocks.

---

# 2️⃣ **Installation & Setup (Local Environment)**

### Install Python dependencies:

```bash
pip install langchain
pip install langchain-openai
pip install langchain-community
pip install langchain-aws
pip install boto3
```

For Bedrock users:

```bash
pip install langchain-aws
```

### Configure AWS:

```bash
aws configure
```

Provide:

* Access key
* Secret key
* Region

Now you're ready to use Bedrock models with LangChain.

---

# 3️⃣ **“Hello World” LangChain App**

This helps you understand the simplest app you can build.

### Example using Amazon Bedrock model (Nova/Claude/Llama):

```python
from langchain_aws import ChatBedrock

llm = ChatBedrock(
    model_id="amazon.nova-lite-v1",
)

response = llm.invoke("Explain cloud computing in simple words.")
print(response)
```

👉 You just built your first LangChain app!

---

# 4️⃣ **Understanding Core Concepts**

LangChain has 6 fundamental building blocks:

1. **Schema**
2. **Models**
3. **Runnables**
4. **Prompts**
5. **Memory**
6. **Chains**

Let’s explain each in very simple words.

---

## ⭐ 4.1 Schema

Schema defines the **structure** of inputs and outputs.

Examples:

* Chat messages
* Inputs
* Output formats (JSON, text)
* Document objects

Schema ensures consistency.

---

## ⭐ 4.2 Models

LLMs used inside LangChain.

Examples:

* ChatBedrock (Nova, Claude, Llama)
* ChatOpenAI
* ChatGoogle
* ChatMistral

LangChain makes switching models easy:

```python
llm = ChatBedrock(model_id="anthropic.claude-3-sonnet-v1")
```

Then replace 1 line to switch models.

---

## ⭐ 4.3 Runnables (LangChain v0.1+)

Runnables allow chaining steps like a pipeline.

Example:

```python
chain = prompt | llm | parser
```

The `|` operator means **pass output of one step to next**.

Runnables are the core of new LangChain.

---

## ⭐ 4.4 Prompts

Prompts are **templates** that guide your LLM.

Example:

```python
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple words."
)
```

Prompts ensure consistent results.

---

## ⭐ 4.5 Memory

LLMs forget previous messages.
LangChain adds memory to maintain conversation.

Types:

* ConversationBufferMemory
* ConversationSummaryMemory
* VectorStoreMemory

Memory enables chatbots that remember context.

---

## ⭐ 4.6 Chains

Chains combine multiple steps into one workflow.

Example:

* Input → Prompt → LLM → Output
* Document → Split → Embed → Store → Query → LLM

Chains help you reuse logic anywhere.

---

# 5️⃣ **Creating Custom Chains**

You can build your own chain step-by-step.

### Example:

```python
from langchain.prompts import PromptTemplate
from langchain_aws import ChatBedrock
from langchain_core.runnables import RunnableSequence

prompt = PromptTemplate.from_template(
    "Rewrite the following text professionally:\n\n{text}"
)

llm = ChatBedrock(model_id="amazon.nova-pro-v1")

chain = RunnableSequence(
    first = prompt,
    last = llm
)

print(chain.invoke({"text": "I need help quickly!"}))
```

👉 You created a reusable custom chain.

---

# 6️⃣ **JSON Parser, XML Parser, List Parser (Output Parsers)**

LangChain provides **parsable output** to get structured results.

---

## ⭐ 6.1 JSON Output Parser

```python
from langchain.output_parsers import JsonOutputParser

parser = JsonOutputParser()
```

Prompt example:

```
Return output in JSON:
{
  "title": "",
  "summary": ""
}
```

---

## ⭐ 6.2 XML Parser

Used less often, but still supported:

```python
from langchain.output_parsers.xml import XMLOutputParser
```

---

## ⭐ 6.3 List Parser

Useful for bullet-point extraction.

```python
from langchain.output_parsers import CommaSeparatedListOutputParser

parser = CommaSeparatedListOutputParser()
```

---

# 7️⃣ **Output Parsers (Detailed Explanation)**

Output parsers help you convert LLM text → structured data.

Types include:

### ✔ JSON Output Parser

For API responses.

### ✔ StructuredOutputParser

For strict field-level validation.

### ✔ ListOutputParser

Extracts lists.

### ✔ XMLOutputParser

Parses XML results.

### ✔ Dataclass Parser

Map output to Python dataclass.

### ✔ Retry Parsers

Retry failed outputs automatically.

These ensure your application gets clean, usable data.

---

# 8️⃣ **Integrations & Tool Support**

LangChain integrates with many systems to create intelligent workflows.

---

## ⭐ 8.1 Vector Databases

LangChain supports:

* Pinecone
* FAISS
* Chroma
* Weaviate
* OpenSearch
* DynamoDB

Essential for RAG.

---

## ⭐ 8.2 Document Loaders (built-in)

Load files from:

* PDFs
* Word docs
* HTML
* Websites
* Notion
* Google Drive
* S3

Example:

```python
from langchain_community.document_loaders import PyPDFLoader
docs = PyPDFLoader("file.pdf").load()
```

---

## ⭐ 8.3 Tools & Agents

Tools allow LLMs to “take actions” like:

* Searching
* Calling APIs
* Accessing databases
* Executing functions

Agents choose which tool to use automatically.

Example:

```python
from langchain.agents import load_tools, initialize_agent

tools = load_tools(["llm-math"])
agent = initialize_agent(tools, llm, agent="conversational-react-description")
```

---

## ⭐ 8.4 AWS Bedrock Integration

```python
from langchain_aws import ChatBedrock

llm = ChatBedrock(model_id="amazon.nova-pro-v1")
```

LangChain + Bedrock = enterprise-ready GenAI.

---

# 🎉 **Final Summary — LangChain in One View**

LangChain provides everything needed to build full GenAI applications:

| Feature          | Purpose                                  |
| ---------------- | ---------------------------------------- |
| **Models**       | Connect to LLMs like Nova, Claude, Llama |
| **Prompts**      | Create structured instructions           |
| **Memory**       | Keep conversation history                |
| **Chains**       | Build workflows                          |
| **Runnables**    | Modern pipeline architecture             |
| **Parsers**      | JSON/XML/List/structured outputs         |
| **Tools**        | Connect LLM to external systems          |
| **Integrations** | Vector DBs, file loaders, APIs           |

LangChain = **LLM application development framework**.

---
