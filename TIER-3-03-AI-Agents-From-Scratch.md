# TIER 3-03: AI Agents From Scratch
## Building Thinking Systems

---

## What's an Agent?

An **agent** is an AI system that:
1. **Observes** its environment/input
2. **Thinks** about what to do
3. **Decides** which action to take
4. **Takes action** (calls tools)
5. **Observes** the result
6. **Repeats** until goal reached

Think: "Agent" like a human solving a problem step-by-step.

---

## Agent Architecture

```
Input
  ↓
LLM (thinks about what to do)
  ↓
Decides: Use tool X with args Y
  ↓
Execute: Call tool X(Y)
  ↓
Observe: Got result Z
  ↓
Update conversation with result
  ↓
LLM thinks again with new info
  ↓
Repeat until done
  ↓
Final output
```

---

## Simple Agent Example

```python
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Define tools
@tool
def calculator(expr: str) -> float:
    """Calculate math"""
    return eval(expr)

@tool
def search(query: str) -> str:
    """Search for information"""
    return f"Found info about {query}"

# Create agent
llm = ChatOpenAI(model="gpt-4")
tools = [calculator, search]

# Prompt for agent
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools to help users."),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# Create agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create executor
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Use it
result = executor.invoke({"input": "What's 100+50? And search for AI"})
print(result)
```

---

## Agent Patterns

### Pattern 1: ReAct (Reasoning + Acting)
```
Thought: What do I need to do?
Action: Use tool X
Observation: Got result Y
Thought: Do I need more info?
...repeat...
Final Answer: Here's the answer
```

### Pattern 2: Plan-and-Execute
```
Planning:
1. First do X
2. Then do Y
3. Finally do Z

Execution:
→ Do X
→ Do Y
→ Do Z

Answer based on all results
```

### Pattern 3: Tool-Use Loop
```
Loop until done:
- Ask LLM what to do
- Execute suggested tool
- Give result back to LLM
- Check if done
```

---

## Multi-Step Agent Example

```python
from langchain.agents import AgentExecutor, create_tool_calling_agent

@tool
def get_user_info(user_id: str) -> str:
    """Get user information"""
    return f"User {user_id}: Name=John, Age=30, Premium=Yes"

@tool
def check_balance(user_id: str) -> str:
    """Check account balance"""
    return f"Balance for {user_id}: $1,234.56"

@tool
def process_refund(user_id: str, amount: str) -> str:
    """Process refund"""
    return f"Refund of ${amount} processed for {user_id}"

# Agent steps through tools automatically
tools = [get_user_info, check_balance, process_refund]
agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools)

# User query that needs multiple steps
result = executor.invoke({
    "input": "Check if user123 is eligible for refund and process $100 if balance > $500"
})

# Agent will:
# 1. Call get_user_info("user123")
# 2. Call check_balance("user123")
# 3. Decide if eligible
# 4. Call process_refund if eligible
# 5. Return result
```

---

## Agent Memory (Conversation)

```python
from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_tool_calling_agent

memory = ConversationBufferMemory(return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are helpful"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# Multi-turn conversation
executor.invoke({"input": "What's 100+50?"})
executor.invoke({"input": "Double that result"})  # Knows it's 300
```

---

## Agent with State Management

```python
from langchain_core.messages import HumanMessage, AIMessage
from typing import Annotated

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    iterations: int

def agent_step(state: AgentState):
    # Get current context
    latest_message = state["messages"][-1]
    
    # Call LLM with all context
    response = llm_with_tools.invoke(state["messages"])
    
    # If tool called, execute
    if response.tool_calls:
        for call in response.tool_calls:
            tool_result = tools[call['name']].invoke(call['args'])
            state["messages"].append(ToolMessage(...))
    
    # Update state
    state["messages"].append(response)
    state["iterations"] += 1
    
    return state

# Run agent with state
state = {
    "messages": [HumanMessage("What's the weather?")],
    "iterations": 0
}

while state["iterations"] < 5:
    state = agent_step(state)
    if not state["messages"][-1].tool_calls:
        break

print(state["messages"][-1].content)  # Final answer
```

---

## Error Recovery

```python
from langchain.agents import AgentExecutor, create_tool_calling_agent

def handle_tool_error(error):
    """Handle tool execution errors"""
    return f"Tool error: {str(error)}. Please try again."

agent = create_tool_calling_agent(llm, tools, prompt)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors="Check your output and try again",
    handle_tool_error=handle_tool_error,
    max_iterations=10
)

# Even if tools fail, agent continues gracefully
result = executor.invoke({"input": "Do something complex"})
```

---

## Production Agent Considerations

1. **Timeouts**: Set max_iterations
2. **Cost**: Monitor tool calls (expensive!)
3. **Safety**: Validate tool inputs
4. **Logging**: Track what agent does
5. **Fallback**: What if tool fails?

---

## Self-Check

Can you:

- [ ] Explain what an agent is?
- [ ] Create a simple agent?
- [ ] Add tools to an agent?
- [ ] Handle multi-step tasks?
- [ ] Add memory to an agent?

Ready for **[TIER-3-04-LangGraph-and-Workflows.md](TIER-3-04-LangGraph-and-Workflows.md)** →

Next: Build stateful, graph-based workflows.
