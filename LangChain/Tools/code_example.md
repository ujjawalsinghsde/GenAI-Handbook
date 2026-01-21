# 📘 **Tools in LangChain**

---

# **1. Installation**

```bash
pip install langchain langchain-core langchain-community langchain-experimental pydantic duckduckgo-search
```

---

# **2. Using Built-In Tools**

LangChain provides many ready-made tools like search, shell, SQL, email, GitHub, and more.

Below are the most important ones.

---

# **2.1 DuckDuckGo Search Tool**

### ✔ Purpose

Fetch live news or web search results.

### ✔ Code

```python
# Import DuckDuckGo Search Tool
from langchain_community.tools import DuckDuckGoSearchRun

# Create the tool instance
search_tool = DuckDuckGoSearchRun()

# Invoke the tool
results = search_tool.invoke("top news in india today")

print(results)
```

### ✔ Inspect tool metadata

```python
print(search_tool.name)         # "duckduckgo_search"
print(search_tool.description)  # Description of tool
print(search_tool.args)         # Expected arguments
```

---

# **2.2 Shell Command Tool (⚠ Use carefully)**

### ✔ Purpose

Execute OS-level shell commands.

### ✔ Code

```python
from langchain_community.tools import ShellTool

shell_tool = ShellTool()

# Example: List directory files
results = shell_tool.invoke("ls")
print(results)
```

⚠ Use carefully in production. Restrict allowed commands.

---

# **3. Creating Custom Tools**

LangChain provides **3 ways** to create tools:

1. `@tool` decorator
2. `StructuredTool` with Pydantic
3. Subclassing `BaseTool`

Below are all three methods with clean, corrected code.

---

# **3.1 Method 1 — Creating Tools Using `@tool` Decorator (Simplest)**

### ✔ Code

```python
from langchain_core.tools import tool

@tool
def multiply(x: int, y: int) -> int:
    """
    Multiply two integers and return the result.
    """
    return x * y

print(multiply.name)
print(multiply.description)
print(multiply.args)
```

---

# **3.2 Method 2 — StructuredTool with Pydantic (Production Safe)**

### ✔ Purpose

When you need **strict input validation** and a cleaner schema.

### ✔ Code

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
    description="Adds two numbers together"
)

print(add_tool.name)
print(add_tool.description)
print(add_tool.args)
```

---

# **3.3 Method 3 — Creating Tools by Subclassing `BaseTool` (Most Advanced)**

### ✔ Purpose

Use this method when:

* You need async logic
* Tools require internal state
* Tools are complex

### ✔ Code

```python
from langchain.tools import BaseTool

class DoctorSearchTool(BaseTool):
    name = "doctor_search"
    description = "Returns doctors for a given specialization."

    def _run(self, specialization: str):
        # Example static logic (replace with DB/API calls)
        doctors = {
            "dental": ["Dr. Mehta", "Dr. Roy"],
            "cardiology": ["Dr. Kapoor", "Dr. Sharma"]
        }

        return doctors.get(specialization.lower(), "No doctors available.")

    async def _arun(self, specialization: str):
        raise NotImplementedError("Async not supported for this tool")

# Usage
tool = DoctorSearchTool()
print(tool.invoke("dental"))
```

---

# **4. Toolkits in LangChain**

A Toolkit is a collection of related tools bundled together.

### ✔ Example Math Toolkit

```python
# Re-use multiply & add tools
math_toolkit = [
    add_tool,
    multiply
]

print([tool.name for tool in math_toolkit])
```

You can create domain-specific toolkits:

* Hospital toolkit
* E-commerce toolkit
* Finance toolkit
* Data engineering toolkit

---

# **5. Tools + Models = Agents**

Tools become powerful when combined with LLMs.

Example — using a tool with an LLM:

```python
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, initialize_agent, AgentType

llm = ChatOpenAI(model="gpt-4o-mini")

tools = [search_tool, multiply]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Example: agent will decide to call multiply tool
response = agent.invoke({"input": "What is 25 times 4?"})
print(response)
```

LLM decides → selects tool → tool runs → LLM continues → returns answer.

This is the foundation of Agents.

---

# **6. Full Combined Code (Ready for Reference & Runbook)**

Below is the complete combined code block (cleaned + commented):

```python
# ---------------------------
# Installation
# ---------------------------
# pip install langchain langchain-core langchain-community langchain-experimental duckduckgo-search pydantic


# ---------------------------------------
# 1. Built-In Tools
# ---------------------------------------
from langchain_community.tools import DuckDuckGoSearchRun, ShellTool

search_tool = DuckDuckGoSearchRun()
print(search_tool.invoke("latest AI news"))  # Web search example

shell_tool = ShellTool()
print(shell_tool.invoke("ls"))               # Shell command example (caution!)


# ---------------------------------------
# 2. Custom Tools — Method 1 (@tool)
# ---------------------------------------
from langchain_core.tools import tool

@tool
def multiply(x: int, y: int) -> int:
    """Multiply two integers."""
    return x * y


# ---------------------------------------
# 3. Custom Tools — Method 2 (StructuredTool)
# ---------------------------------------
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class AdditionInput(BaseModel):
    a: int
    b: int

def add_numbers(a: int, b: int):
    return a + b

add_tool = StructuredTool.from_function(
    func=add_numbers,
    args_schema=AdditionInput,
    description="Add two numbers"
)


# ---------------------------------------
# 4. Custom Tools — Method 3 (BaseTool)
# ---------------------------------------
from langchain.tools import BaseTool

class DoctorSearchTool(BaseTool):
    name = "doctor_search"
    description = "Return list of doctors by specialization."

    def _run(self, specialization: str):
        doctors = {
            "dental": ["Dr. Mehta", "Dr. Roy"],
            "cardiology": ["Dr. Sharma", "Dr. Kapoor"]
        }
        return doctors.get(specialization.lower(), "No doctors found.")

    async def _arun(self, specialization: str):
        raise NotImplementedError()

doctor_tool = DoctorSearchTool()


# ---------------------------------------
# 5. Toolkits Example
# ---------------------------------------
math_toolkit = [multiply, add_tool]


# ---------------------------------------
# 6. Using Tools with Agents
# ---------------------------------------
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

llm = ChatOpenAI(model="gpt-4o-mini")

agent = initialize_agent(
    tools=[search_tool, multiply, add_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

result = agent.invoke({"input": "What is 32 + 44? Use tool if needed."})
print(result)
```

---
