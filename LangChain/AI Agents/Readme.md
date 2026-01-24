# **📘 AI Agents**

# **1. Introduction to AI Agents**

An **AI Agent** is a system that can:

* Understand a goal stated by a user
* Reason about the steps needed to fulfill it
* Call external tools, APIs, or functions to gather information
* Interpret results and decide what to do next
* Continue iterating until the goal is achieved

Think of an agent as an **LLM with decision-making and action-taking powers**.

### **Why Do We Need Agents?**

Most real-world tasks such as:

* Planning travel
* Booking tickets
* Extracting data
* Comparing prices
* Retrieving live information
* Handling workflows with multiple dependencies

…require **multiple steps** and **multiple tools or sources**.

Agents convert these complex, multi-step workflows into a natural conversation:

> “Plan my Goa trip on a budget from May 1–7.”
> → The agent thinks, searches, compares, plans, and returns a full itinerary.

---

# **2. Core Characteristics of AI Agents**

AI Agents are defined by five key properties:

### **1. Goal-Driven Behaviour**

The agent receives an objective, not a detailed set of steps.

### **2. Multi-Step Reasoning**

Agents break tasks into smaller steps automatically.

### **3. Tool Awareness**

Agents select the right tool (search API, calculator, weather API, DB query, etc.) based on user intent.

### **4. Context Maintenance**

Agents remember previous observations, thoughts, and results.

### **5. Adaptivity**

If a tool fails or new information comes in, the agent reshapes the plan.

---

# **3. Understanding the REACT Framework**

**REACT** stands for **Reasoning + Acting**.

This is the heart of modern agents.

An agent does not produce a final answer in one shot.
Instead, it works in a loop:

```
Thought → Action → Observation → Thought → ...
```

### **3.1 Components**

#### **Thought**

Internal reasoning
Example:
“I need to find the capital of France first.”

#### **Action**

Decision about which tool to use
Example:
Action: search_tool
Action Input: "capital of France"

#### **Observation**

Result returned by the tool
Example:
“Paris is the capital of France.”

#### **Final Answer**

When the agent concludes the task
Example:
“Paris is the capital of France and its population is approx. 2.1M.”

### **3.2 Why REACT Is Important**

* Enables transparency
* Handles multi-step problems
* Allows modular, tool-based workflows
* Supports long chains of reasoning
* Creates explainable agents

---

# **4. Architecture of an AI Agent in LangChain**

The full system consists of:

1. **LLM (core reasoning engine)**
2. **Prompt (rules + instructions)**
3. **Tools (actions the agent can take)**
4. **Agent (logic that chooses the next step)**
5. **Agent Executor (controller of the loop)**
6. **Scratchpad (memory of actions & results)**

Let’s break each component in detail.

---

# **5. Agent vs AgentExecutor**

## **5.1 Agent**

The agent decides:

* What to think
* What tool to use
* What input to provide
* When the task is done

The agent does **not** execute tools.
It only **plans** and **selects actions**.

The agent relies on:

* LLM reasoning
* Prompt structure
* Available tools
* Scratchpad history

---

## **5.2 AgentExecutor**

The executor manages the entire lifecycle:

1. Receives the user query
2. Sends query + scratchpad to Agent
3. Gets “Action”
4. Runs the tool
5. Receives “Observation”
6. Appends to scratchpad
7. Sends updated scratchpad back to Agent
8. Repeats
9. Stops when Agent returns “Final Answer”

---

# **6. Flow of an AI Agent (Step-By-Step)**

Below is a clean, readable architecture flow:

```
┌───────────────────────────────┐
│         User Query            │
└───────────────────────────────┘
               ↓
┌───────────────────────────────┐
│        Agent Executor         │
└───────────────────────────────┘
               ↓
┌───────────────────────────────┐
│  Agent (LLM + Prompt + Tools) │
└───────────────────────────────┘
               ↓ Thought
┌───────────────────────────────┐
│     Decide Next Action        │
└───────────────────────────────┘
               ↓
┌───────────────────────────────┐
│       Execute Tool            │
└───────────────────────────────┘
               ↓ Observation
┌───────────────────────────────┐
│      Update Scratchpad        │
└───────────────────────────────┘
               ↓
If action needed → loop  
If done → Final Answer
```

---

# **7. Creating an Agent in LangChain**

## **7.1 Steps to Build**

### **1. Load LLM**

The LLM performs reasoning (Thought → Action decisions).

### **2. Define Tools**

Each tool must have:

* A name
* A clear description
* A function to execute

Examples:

* Web search tool
* Weather tool
* Currency converter
* Database query tool

### **3. Create Prompt**

The prompt defines:

* How the agent reasons
* How thoughts and actions are formatted
* How to use tools
* When to stop

### **4. Build Agent using create_react_agent**

This method links:

* LLM
* Tools
* Prompt

### **5. Wrap it with AgentExecutor**

To orchestrate:

* Thought-action-observation loops
* Scratchpad updates
* Final answer detection

---

# **8. Example: Multi-Step Agent Execution**

Let’s walk through the reasoning trace of a typical agent.

### **User Query**

“What is the capital of France and what is its population?”

### **Step 1**

**Thought:**
I need to find the capital of France first.

**Action:**
search_tool

**Action Input:**
"capital of France"

### **Step 2**

**Observation:**
“Paris is the capital of France.”

---

### **Step 3**

**Thought:**
Now I need the population of Paris.

**Action:**
search_tool

**Action Input:**
"population of Paris"

### **Step 4**

**Observation:**
“Paris has a population of approximately 2.1 million.”

---

### **Step 5**

**Thought:**
I now know the final answer.

### **Final Answer**

“Paris is the capital of France and has a population of approximately 2.1 million.”

---

# **9. Adding Custom Tools**

Agents become truly powerful when extended with custom tools.

You can add:

* Weather APIs
* Finance APIs
* Ticket-booking calls
* Currency conversion
* Internal services
* Database queries

### **Flow of a Custom Tool**

1. Agent identifies missing information
2. Chooses the right tool
3. Sends structured input
4. Receives structured output
5. Updates scratchpad
6. Decides next action

### **Example: Currency Conversion**

User: “Convert 10 USD to INR”

Agent thinking:

1. Find USD→INR rate
2. Multiply amount * rate
3. Return final converted value

The agent automatically discovers and executes each step.

---

# **10. Designing End-to-End Real-World Agents**

A production-grade agent incorporates:

## **10.1 Orchestration Layer**

* Manages full workflow
* Handles multiple steps
* Manages retries and errors

## **10.2 Reasoning Layer**

Uses structured patterns like:

* REACT
* Plan-and-execute
* Decomposition strategies

## **10.3 Tooling Layer**

Integrates all APIs and services:

* External APIs
* Internal microservices
* DB connections
* Utility functions

## **10.4 Memory Layer**

Includes:

* Scratchpad
* Conversation memory
* Long-term state

## **10.5 Safety Layer**

Controls:

* What tools can be used
* Parameter validation
* Preventing unwanted actions

---

# **11. Advanced Concepts**

### **Delegation**

Agents can delegate work to other agents.

### **Hierarchical Planning**

A planner agent creates steps; an executor agent performs them.

### **Tool Routing**

Choosing the correct tool based on validated intent.

### **Self-Correction**

Agents reason about incorrect tool results and re-query or retry.

---

# **12. Practical Best Practices**

### **Prompt Design**

* Keep instructions explicit
* Define Thought/Action/Observation clearly
* Avoid ambiguity

### **Tool Design**

* Keep each tool single-purpose
* Return predictable structured outputs

### **Observability**

* Store traces to debug agent behavior
* Log tool failures

### **Validation**

* Validate all tool inputs and outputs
* Add rate-limits and boundaries

### **Fail-Safes**

* Add fallback tools
* Add timeouts
* Add action limits

---

# **13. Final Summary**

Building an end-to-end AI Agent in LangChain requires integrating:

* **LLMs** for reasoning
* **Prompts** for structure
* **Tools** for actions
* **Scratchpads** for memory
* **AgentExecutor** for controlling loops

Agents support:

* Multi-step reasoning
* Autonomous planning
* External tool execution
* Real-world workflow automation

---

