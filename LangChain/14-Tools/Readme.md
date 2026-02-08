# Tools

## Why Do We Need Tools in LangChain?

Large Language Models have strengths in reasoning and language generation but lack the capability to execute actions in external systems. This limitation prevents them from:

* Calling APIs
* Executing Python code
* Accessing databases
* Searching the internet
* Sending emails
* Running OS commands

Think of LLMs like:

* **Brain + Mouth**, but **no Hands + Legs**

### ✔ Tools = Hands + Legs for LLM

Tools allow LLMs to:

* Interact with external systems
* Fetch live data
* Execute business logic
* Run commands
* Perform actions intelligently

Tools complete the missing piece required to build **Agents**.

---

# **2. What Are Tools in LangChain? (Definition)**

A **Tool** in LangChain is:

> *A callable function (Python function or class) wrapped in special LangChain metadata so that an LLM can decide when and how to call it.*

Each tool contains:

* A **name**
* A **description** (must be clear)
* **Input arguments** with types
* The **logic to execute**

When using Agents, the LLM can automatically:

1. Understand the task
2. Select the appropriate tool
3. Call the tool
4. Observe results
5. Continue reasoning

So tools are essential for **action-oriented AI systems**.

---

# **3. Types of Tools in LangChain**

Tools fall into two main categories:

---

## **3.1 Built-in Tools (Predefined by LangChain)**

LangChain ships with many ready-made tools for common tasks:

### **🔎 Information / Search Tools**

* DuckDuckGo Search
* Wikipedia Search
* Google Search (through API wrappers)

### **💻 Code Execution Tools**

* Python REPL (execute Python code)
* Shell-based tools (run terminal commands)

### **📧 Communication Tools**

* Gmail tool
* Slack tool
* Twilio SMS
* Zapier automation tools

### **📦 Database Tools**

* SQL Database Query tool
* VectorDB search tools
* ElasticSearch tool

### **🌐 Web Interaction Tools**

* Web browsing tools
* Fetch URL tool

### **💼 Business Integrations**

* GitHub
* Notion
* Google Drive
* Office365

These tools save time and are best for **quick experiments**, POCs, and common integrations.

---

## **3.2 Custom Tools (User-defined)**

Custom tools are needed when you want an LLM to operate **your business logic**:

Examples:

* Fetch customer data from a private API
* Book appointment
* Check hospital availability
* Run a financial model
* Query internal SQL / MongoDB
* Analyze logs
* Call ML models (LLM → ML model tool)

Custom tools provide **full flexibility** and are production-ready.

---

# **4. How Tools Work Internally (Simple Mental Model)**

```
User Query → LLM → Decide if a tool is needed → Tool executes → Sends result → LLM continues
```

Example:
**User:** “What is the latest news about Tesla?”
**LLM:** “I need web search → call DuckDuckGo tool”
**Tool:** returns news articles
**LLM:** summarises and answers

This “reason → act → observe → answer” cycle is the foundation of LangChain Agents.

---

# **5. Creating Tools in LangChain (Three Methods)**

LangChain provides three ways.

---

# **5.1 Method 1 — @tool Decorator (Fastest & Easiest)**

Best for:

* Simple functions
* Quick prototyping
* Readable code

### ✔ Steps:

1. Write a Python function
2. Add type hints
3. Add clear docstring
4. Decorate with `@tool`

### Example:

```python
from langchain.tools import tool

@tool
def multiply(x: int, y: int) -> int:
    """Multiply two integers and return the result."""
    return x * y
```

After decoration:

* Tool has `.name = "multiply"`
* Description is extracted from docstring
* Input schema automatically derived

**LLMs can now call this tool.**

---

# **5.2 Method 2 — StructuredTool with Pydantic (Production Safe)**

Use this when:

* You need **strong input validation**
* Tool must enforce strict JSON schema
* Input is complex (objects, lists, etc.)

### Example:

```python
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool

class AdditionInput(BaseModel):
    a: int = Field(..., description="First number")
    b: int = Field(..., description="Second number")

def add_numbers(a: int, b: int):
    return a + b

add_tool = StructuredTool.from_function(
    func=add_numbers,
    args_schema=AdditionInput,
    description="Adds two numbers"
)
```

This ensures:

* No invalid inputs
* Clear documentation
* Useful in real-world APIs

---

# **5.3 Method 3 — Inherit BaseTool (Maximum Flexibility)**

Use when:

* You need async tools
* You need concurrency
* Tool needs internal state
* Complex business logic

### Example:

```python
from langchain.tools import BaseTool

class MedicalTool(BaseTool):
    name = "doctor_lookup"
    description = "Find doctor details in the database"

    def _run(self, specialization: str):
        # custom logic
        return f"Doctor list for {specialization}"

    async def _arun(self, specialization: str):
        raise NotImplementedError("Async not supported")
```

This method gives:

* Full control
* Ideal for enterprise systems

---

# **6. Toolkits in LangChain**

A **Toolkit** is a collection of related tools packaged together.

### Example:

Math Toolkit = [add_tool, multiply_tool]
Google Drive Toolkit = upload + search + read

Benefits:

* Group tools by domain
* Easy integration
* Easy reuse across agents

You can create your own toolkit:

```python
custom_toolkit = [add_tool, multiply_tool, subtraction_tool]
```

---

# **7. Tools + LLM = Agents (How They Combine)**

A complete agent system requires:

| Component | Role                                                |
| --------- | --------------------------------------------------- |
| **LLM**   | Think, plan, analyze                                |
| **Tools** | Perform actions                                     |
| **Agent** | Bridges LLM with tools, manages reasoning & actions |

Workflow:

1. **LLM receives the prompt**
2. **Agent evaluates** whether tools are needed
3. **Agent selects the tool**
4. **Tool executes** (API, DB, Code, etc.)
5. **Agent passes result back to LLM**
6. **LLM generates final answer**

Tools are the main building block.
Agent is the controller.

---

# **8. Practical Examples of Tools (Real Use Cases)**

### **Healthcare Chatbot**

* Tool 1 → search diseases
* Tool 2 → check doctor availability
* Tool 3 → book appointment
* Tool 4 → verify patient details

### **E-commerce Agent**

* searchProduct tool
* addToCart tool
* trackOrder tool

### **Finance Agent**

* fetchStockPrice tool
* calculatePortfolio tool

### **Data Engineering Agent**

* runSparkJob tool
* queryRedshift tool
* generateParquet tool

---

# **9. Best Practices for Designing Tools**

### ✔ Keep tool descriptions short & actionable

LLM reads descriptions first.

### ✔ Define strict input types

Type hints avoid LLM mistakes.

### ✔ Add docstrings with intention

LLM uses docstrings to understand tool purpose.

### ✔ Avoid writing business logic inside LLM

Always place logic in tools.

### ✔ Keep tools atomic (single responsibility)

One tool = one action.

### ✔ Validate inputs when accepting user data

### ✔ If tool uses external API, handle exceptions

---

# **10. Summary Cheat Sheet (Quick Revision)**

| Topic            | Summary                                   |
| ---------------- | ----------------------------------------- |
| Tools            | Functions LLM can call to perform actions |
| Why?             | LLMs cannot act; tools allow actions      |
| Types            | Built-in + Custom                         |
| Creation Methods | `@tool`, StructuredTool, BaseTool         |
| Toolkits         | Groups of similar tools                   |
| Agent Role       | Select tools → Execute → Return result    |
| Use Cases        | API calls, DB queries, workflows, apps    |

Tools → extend LLM capability
Agents → orchestrate LLM + tools
