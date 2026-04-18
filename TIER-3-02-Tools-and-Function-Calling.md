# TIER 3-02: Tools and Function Calling
## Making LLMs Take Actions

---

## The Problem

LLMs are great at talking, but they can't:
- Access the internet (real-time data)
- Calculate precise math
- Access databases
- Send emails
- Call APIs

**Solution: Give them tools to use.**

---

## What Are Tools?

A **tool** is a function the LLM can call:

```
User: "What's the weather?"
LLM thinks: "I need to call the weather_tool"
System: Calls weather API
System: Returns result
LLM: "It's 72°F and sunny"
```

---

## Simple Tool Example

```python
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Calculate a math expression"""
    return str(eval(expression))

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city"""
    # In real app, call weather API
    return f"Weather in {city}: 72°F, sunny"

# LLM can now use these tools!
tools = [calculator, get_weather]
```

---

## Function Calling (Modern Approach)

LLMs can output structured calls to functions:

```python
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

# Define tools
tools = [calculator, get_weather, ...]

# Bind tools to LLM
llm_with_tools = llm.bind_tools(tools)

# LLM can now call tools
response = llm_with_tools.invoke("What's 2+2?")
# Response includes: call calculator("2+2")
```

---

## Tool Chains (Action Loop)

```
Step 1: User question
    ↓
Step 2: LLM decides which tool to call
    ↓
Step 3: Execute tool
    ↓
Step 4: Return result to LLM
    ↓
Step 5: LLM generates final answer
    ↓
Final Answer
```

---

## Real Example: Calculator Tool

```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

@tool
def calculator(expression: str) -> float:
    """Evaluate a math expression"""
    try:
        return float(eval(expression))
    except:
        return "Invalid expression"

llm = ChatOpenAI(model="gpt-4")
llm_with_tools = llm.bind_tools([calculator])

# Use it
response = llm_with_tools.invoke([
    HumanMessage(content="What is 47 * 23?")
])

print(response.tool_calls)
# Output: [{'name': 'calculator', 'args': {'expression': '47*23'}}]
```

---

## Building an Agent (Loop)

```python
from langchain_core.messages import HumanMessage, ToolMessage

def run_agent(user_query):
    messages = [HumanMessage(content=user_query)]
    
    while True:
        # Step 1: Get response from LLM
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        
        # Step 2: Check if tool was called
        if not response.tool_calls:
            # No tool calls - return final answer
            return response.content
        
        # Step 3: Execute each tool call
        for tool_call in response.tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']
            
            # Find and execute tool
            tool = next(t for t in tools if t.name == tool_name)
            result = tool.invoke(tool_args)
            
            # Add result back to conversation
            messages.append(ToolMessage(
                content=str(result),
                tool_call_id=tool_call['id']
            ))

# Use it
answer = run_agent("What is 47 * 23?")
```

---

## Common Tools

### Web Search
```python
@tool
def web_search(query: str) -> str:
    """Search the web for information"""
    # Use Google Search API or DuckDuckGo
    from googlesearch import search
    results = list(search(query, num_results=3))
    return "\n".join(results)
```

### Database Query
```python
@tool
def query_database(sql: str) -> str:
    """Query company database"""
    import sqlite3
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    return str(results)
```

### Email
```python
@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email"""
    import smtplib
    # Implementation...
    return "Email sent successfully"
```

### File Operations
```python
@tool
def read_file(path: str) -> str:
    """Read file contents"""
    with open(path, 'r') as f:
        return f.read()

@tool
def write_file(path: str, content: str) -> str:
    """Write to a file"""
    with open(path, 'w') as f:
        f.write(content)
    return "File written"
```

---

## Advanced: Pydantic for Tool Definitions

```python
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class CalculatorInput(BaseModel):
    """Input for calculator"""
    expression: str = Field(description="Math expression to evaluate")

class WeatherInput(BaseModel):
    """Input for weather tool"""
    city: str = Field(description="City name")
    units: str = Field(
        default="fahrenheit",
        description="Temperature units: celsius or fahrenheit"
    )

@tool(args_schema=CalculatorInput)
def calculator(expression: str) -> float:
    """Evaluate math expression"""
    return eval(expression)

@tool(args_schema=WeatherInput)
def get_weather(city: str, units: str = "fahrenheit") -> str:
    """Get weather for a city"""
    # API call...
    return f"Weather in {city}: 72°F"

# LLM now knows exact input format!
```

---

## Error Handling

```python
@tool
def safe_calculator(expression: str) -> str:
    """Calculate safely"""
    try:
        # Validate expression (prevent injection)
        if not all(c in "0123456789+-*/(). " for c in expression):
            return "Invalid characters in expression"
        
        result = eval(expression)
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except SyntaxError:
        return "Error: Invalid syntax"
    except Exception as e:
        return f"Error: {str(e)}"
```

---

## Full Example: Multi-Tool Agent

```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

@tool
def calculator(expr: str) -> float:
    """Calculate math"""
    return eval(expr)

@tool
def search_docs(query: str) -> str:
    """Search company documents"""
    # Simplified search
    docs = {
        "policy": "Return policy: 30 days",
        "hours": "Office hours: 9-5 Mon-Fri",
    }
    return docs.get(query, "Not found")

# Setup
llm = ChatOpenAI(model="gpt-4")
tools = [calculator, search_docs]
llm_with_tools = llm.bind_tools(tools)

# Agent loop
def run_agent(query):
    messages = [HumanMessage(content=query)]
    max_iterations = 5
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        
        if not response.tool_calls:
            return response.content
        
        for call in response.tool_calls:
            tool = next(t for t in tools if t.name == call['name'])
            result = tool.invoke(call['args'])
            messages.append(ToolMessage(
                content=str(result),
                tool_call_id=call['id']
            ))
    
    return "Max iterations reached"

# Use it
print(run_agent("What's our return policy? And what's 100+50?"))
```

---

## Safety Considerations

### 1. Tool Permissions
Only expose necessary tools.

### 2. Input Validation
Always validate tool inputs.

### 3. Rate Limiting
Don't let LLM call tools indefinitely.

### 4. Sensitive Data
Be careful with database/email tools.

---

## Self-Check

Can you:

- [ ] Define a simple tool with @tool decorator?
- [ ] Bind tools to an LLM?
- [ ] Extract tool calls from LLM response?
- [ ] Execute a tool and return result?
- [ ] Build a complete agent loop?

Ready for **[TIER-3-03-AI-Agents-From-Scratch.md](TIER-3-03-AI-Agents-From-Scratch.md)** →

Next: Build intelligent agents that think and act.
