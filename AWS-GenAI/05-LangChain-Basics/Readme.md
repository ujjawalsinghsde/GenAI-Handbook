# LangChain

LangChain is a framework that helps developers build applications using Large Language Models (LLMs). It provides tools, building blocks, and integrations for production-ready AI apps such as chatbots, agents, RAG, and automated workflows.

---

## Introduction to LangChain

### What is LangChain?

LangChain is a Python/JavaScript framework that simplifies working with LLMs including OpenAI, Amazon Bedrock, Anthropic, Google Gemini, Llama/Mistral, and Hugging Face.

LangChain helps build chatbots, RAG systems, agents, LLM-powered APIs, document analysis tools, and multi-step workflows.

### Why LangChain?

LangChain provides application-level primitives around LLMs:

- Prompt templates
- Chains
- Memory
- Agents
- Runnables
- Parsers
- Tools
- Integrations
- Document loaders
- Vector stores

It organizes applications into reusable, testable blocks.

---

# Installation & Setup (Local Environment)

Install Python dependencies:

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

Configure AWS credentials:

```bash
aws configure
```

Provide your Access Key, Secret Key, and Region to use Bedrock models with LangChain.

---

# Hello World LangChain App

Example using an Amazon Bedrock model (Nova/Claude/Llama):

```python
from langchain_aws import ChatBedrock

llm = ChatBedrock(model_id="amazon.nova-lite-v1")

response = llm.invoke("Explain cloud computing in simple words.")
print(response)
```

You have created a simple LangChain application.

---

# Understanding Core Concepts

LangChain has six fundamental building blocks:

1. Schema
2. Models
3. Runnables
4. Prompts
5. Memory
6. Chains

---

### Schema

Schema defines the structure of inputs and outputs (chat messages, input variables, output formats such as JSON or text, and document objects). Schemas ensure consistency across components.

---

### Models

Models are LLM providers used within LangChain. Examples: `ChatBedrock` (Nova, Claude, Llama), `ChatOpenAI`, `ChatGoogle`, `ChatMistral`.

LangChain makes swapping providers simple; change a single `model_id` to switch backends.

---

### Runnables (LangChain v0.1+)

Runnables allow chaining steps into pipelines. Example:

```python
chain = prompt | llm | parser
```

The `|` operator forwards output from one step to the next.

---

### Prompts

Prompts are templates that guide model behavior. Example:

```python
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in simple words."
)
```

---

### Memory

Memory stores conversational state so models can maintain context. Common memory types include `ConversationBufferMemory`, `ConversationSummaryMemory`, and `VectorStoreMemory`.

---

### Chains

Chains combine multiple steps into reusable workflows, for example: Input → Prompt → LLM → Output or Document → Split → Embed → Store → Query → LLM.

---

# Creating Custom Chains

You can construct custom chains by composing prompts, models, and parsers. Example:

```python
from langchain.prompts import PromptTemplate
from langchain_aws import ChatBedrock
from langchain_core.runnables import RunnableSequence

prompt = PromptTemplate.from_template(
    "Rewrite the following text professionally:\n\n{text}"
)

llm = ChatBedrock(model_id="amazon.nova-pro-v1")

chain = RunnableSequence(first=prompt, last=llm)

print(chain.invoke({"text": "I need help quickly!"}))
```

This creates a reusable custom chain.

---

# JSON, XML, and List Parsers (Output Parsers)

LangChain supports parsable outputs to obtain structured results.

### JSON Output Parser

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

### XML Parser

```python
from langchain.output_parsers.xml import XMLOutputParser
```

---

### List Parser

Useful for extracting bullet lists:

```python
from langchain.output_parsers import CommaSeparatedListOutputParser

parser = CommaSeparatedListOutputParser()
```

---

# Output Parsers (Detailed Explanation)

Output parsers convert LLM text into structured data. Common parser types:

### JSON Output Parser

For structured API responses and strict JSON output.

### StructuredOutputParser

For field-level validation and strict schemas.

### ListOutputParser

Extracts enumerated lists from free text.

### XMLOutputParser

Parses XML-formatted outputs.

### Dataclass Parser

Map outputs to Python dataclasses for typed handling.

### Retry Parsers

Retries parsing when outputs do not match expected formats.

These parsers help ensure applications receive reliable, validated data.

---

# Integrations & Tool Support

LangChain integrates with systems to build intelligent workflows.

### Vector Databases

Supported vector stores: Pinecone, FAISS, Chroma, Weaviate, OpenSearch, and DynamoDB — essential for RAG.

---

### Document Loaders (built-in)

Load documents from PDFs, Word, HTML, websites, Notion, Google Drive, S3, and other sources.

Example:

```python
from langchain_community.document_loaders import PyPDFLoader
docs = PyPDFLoader("file.pdf").load()
```

---

### Tools & Agents

Tools enable LLMs to perform actions: search, call APIs, access databases, and execute functions. Agents select tools automatically.

Example:

```python
from langchain.agents import load_tools, initialize_agent

tools = load_tools(["llm-math"])
agent = initialize_agent(tools, llm, agent="conversational-react-description")
```

---

### AWS Bedrock Integration

```python
from langchain_aws import ChatBedrock

llm = ChatBedrock(model_id="amazon.nova-pro-v1")
```

LangChain combined with Bedrock supports enterprise GenAI applications.

---

## Final Summary — LangChain in One View

LangChain provides the primitives required to build GenAI applications:

| Feature          | Purpose                                  |
| ---------------- | ---------------------------------------- |
| Models           | Connect to LLMs like Nova, Claude, Llama |
| Prompts          | Create structured instructions           |
| Memory           | Keep conversation history                |
| Chains           | Build workflows                          |
| Runnables        | Modern pipeline architecture             |
| Parsers          | JSON/XML/List/structured outputs         |
| Tools            | Connect LLM to external systems          |
| Integrations     | Vector DBs, file loaders, APIs           |

LangChain is an application development framework for LLMs.

---
