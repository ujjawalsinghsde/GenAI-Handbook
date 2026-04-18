# TIER 3-04: LangGraph and Workflows
## Building Stateful, Graph-Based Systems

---

## Why LangGraph?

Regular agents are sequential. LangGraph allows:
- **Cycles**: Go back and fix mistakes
- **Branches**: Different paths based on state
- **State Management**: Track everything
- **Visualization**: See what's happening

---

## Core Concepts

### Nodes
Functions in the graph.

### Edges
Connections between nodes (paths).

### State
Shared data between all nodes.

### Graph
The complete workflow.

---

## Simple LangGraph Example

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class State(TypedDict):
    question: str
    answer: str
    iterations: int

# Define nodes
def node_research(state):
    # Do research
    research = f"Researched: {state['question']}"
    return {"answer": research, "iterations": state["iterations"] + 1}

def node_analyze(state):
    # Analyze
    analysis = f"Analysis of: {state['answer']}"
    return {"answer": analysis, "iterations": state["iterations"] + 1}

def node_finalize(state):
    # Final answer
    final = f"Final answer: {state['answer']}"
    return {"answer": final}

# Create graph
graph = StateGraph(State)

# Add nodes
graph.add_node("research", node_research)
graph.add_node("analyze", node_analyze)
graph.add_node("finalize", node_finalize)

# Add edges
graph.add_edge("research", "analyze")
graph.add_edge("analyze", "finalize")
graph.add_edge("finalize", END)

# Set entry point
graph.set_entry_point("research")

# Compile
app = graph.compile()

# Run it
result = app.invoke({"question": "What is AI?", "iterations": 0})
print(result)
```

---

## Conditional Edges (Routing)

```python
from langgraph.graph import StateGraph, END

def should_revise(state):
    """Decide if we need to revise"""
    if state["iterations"] < 3 and "improve" in state["feedback"].lower():
        return "revise"
    return "finalize"

graph = StateGraph(State)

graph.add_node("generate", node_generate)
graph.add_node("review", node_review)
graph.add_node("revise", node_revise)
graph.add_node("finalize", node_finalize)

# Conditional routing
graph.add_edge("generate", "review")
graph.add_conditional_edges(
    "review",
    should_revise,
    {
        "revise": "revise",
        "finalize": "finalize"
    }
)

graph.add_edge("revise", "review")  # Loop back
graph.add_edge("finalize", END)
```

---

## Complex Workflow: Document Analysis

```python
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

class AnalysisState(TypedDict):
    document: str
    summary: str
    sentiment: str
    entities: str
    final_report: str

def extract_entities(state):
    """Extract entities from document"""
    llm = ChatOpenAI()
    entities = llm.invoke(f"Extract entities from: {state['document']}")
    return {"entities": entities.content}

def analyze_sentiment(state):
    """Analyze sentiment"""
    llm = ChatOpenAI()
    sentiment = llm.invoke(f"Analyze sentiment: {state['document']}")
    return {"sentiment": sentiment.content}

def summarize(state):
    """Summarize document"""
    llm = ChatOpenAI()
    summary = llm.invoke(f"Summarize: {state['document']}")
    return {"summary": summary.content}

def create_report(state):
    """Combine all analysis into report"""
    report = f"""
    Summary: {state['summary']}
    Sentiment: {state['sentiment']}
    Entities: {state['entities']}
    """
    return {"final_report": report}

# Build graph
graph = StateGraph(AnalysisState)

graph.add_node("summarize", summarize)
graph.add_node("sentiment", analyze_sentiment)
graph.add_node("entities", extract_entities)
graph.add_node("report", create_report)

# Parallel edges (run simultaneously)
graph.add_edge("summarize", "report")
graph.add_edge("sentiment", "report")
graph.add_edge("entities", "report")

graph.set_entry_point("summarize")
graph.add_edge("report", END)

app = graph.compile()

# Run analysis
result = app.invoke({"document": "Large document text..."})
print(result["final_report"])
```

---

## Loops and Cycles

```python
def revision_needed(state):
    """Check if revision needed"""
    return state["quality"] < 0.8

graph = StateGraph(State)

graph.add_node("generate", generate_content)
graph.add_node("evaluate", evaluate_quality)
graph.add_node("improve", improve_content)

graph.add_edge("generate", "evaluate")
graph.add_conditional_edges(
    "evaluate",
    revision_needed,
    {
        True: "improve",    # Needs improvement
        False: END           # Good enough
    }
)

# Important: Create cycle
graph.add_edge("improve", "evaluate")  # Loop back

app = graph.compile()
result = app.invoke({"content": "", "quality": 0})
```

---

## Human-in-the-Loop

```python
def ask_human(state):
    """Ask human for input"""
    response = input(f"Proceed? (yes/no): ")
    return {"human_approved": response == "yes"}

graph = StateGraph(State)

graph.add_node("generate", generate)
graph.add_node("review", ask_human)
graph.add_node("execute", execute)

graph.add_edge("generate", "review")
graph.add_conditional_edges(
    "review",
    lambda s: "execute" if s["human_approved"] else END,
    {"execute": "execute"}
)

app = graph.compile()
```

---

## Error Handling with LangGraph

```python
def safe_node(state):
    """Node with error handling"""
    try:
        result = risky_operation(state)
        return {"result": result, "error": None}
    except Exception as e:
        return {"result": None, "error": str(e)}

def error_handler(state):
    """Route based on errors"""
    return "retry" if state["error"] else "continue"

graph = StateGraph(State)
graph.add_node("operation", safe_node)
graph.add_node("retry", safe_node)
graph.add_node("continue", next_step)

graph.add_conditional_edges(
    "operation",
    error_handler,
    {"retry": "retry", "continue": "continue"}
)
```

---

## Real Production Example: Customer Support

```python
class SupportState(TypedDict):
    customer_query: str
    faq_answer: str
    agent_response: str
    ticket_created: bool
    final_response: str

# Nodes
def check_faq(state):
    """Check if answer in FAQ"""
    answer = search_faq(state["customer_query"])
    return {"faq_answer": answer}

def needs_agent(state):
    """Decide if needs human agent"""
    return state["faq_answer"] == "No answer found"

def get_agent_help(state):
    """Get help from human agent"""
    response = contact_agent(state["customer_query"])
    return {"agent_response": response, "ticket_created": True}

def send_faq(state):
    """Send FAQ answer"""
    return {"final_response": state["faq_answer"], "ticket_created": False}

# Graph
graph = StateGraph(SupportState)

graph.add_node("faq", check_faq)
graph.add_node("agent", get_agent_help)
graph.add_node("faq_reply", send_faq)

graph.add_edge("faq", "agent_decision")  # Not a node, using conditional
graph.add_conditional_edges(
    "faq",
    needs_agent,
    {True: "agent", False: "faq_reply"}
)

graph.add_edge("agent", END)
graph.add_edge("faq_reply", END)

app = graph.compile()
```

---

## Visualization

```python
# See what the graph looks like
from IPython.display import Image, display

app = graph.compile()
Image(app.get_graph().draw_mermaid_png())
```

---

## Self-Check

Can you:

- [ ] Define a State?
- [ ] Create nodes?
- [ ] Add edges?
- [ ] Create conditional edges?
- [ ] Build cycles/loops?

Ready for **[TIER-3-05-Production-Readiness.md](TIER-3-05-Production-Readiness.md)** →

Next: Deploy and maintain production systems.
