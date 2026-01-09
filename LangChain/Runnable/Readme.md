# 🧩 LangChain Runnables

---

## 1️⃣ Why Runnables Exist (Problem First)

Before **Runnables**, LangChain had many useful components like **LLMs, PromptTemplates, Retrievers, Parsers**, etc.
But the **problem** was how these components worked together.

#### ❌ What was the issue?

* Each component had **different method names**
* Different **input and output formats**
* No common way to connect them

Because of this:

* LangChain had to create **many special chains** (LLMChain, QAChain, SQLChain, etc.)
* Code became **hard to maintain**
* New developers got **confused** about which chain to use
* Custom workflows required **extra glue code**

#### ✅ What Runnables solved

Runnables introduced **one common interface**:

```text
Input → invoke() → Output
```

Now:

* Every component behaves the **same way**
* Any component can connect with any other
* Chains became **simple compositions**, not special classes

👉 **In short:**
Runnables exist to **standardize all components**, reduce complexity, and make LangChain workflows **easy to build, connect, and scale**.

---

## 2️⃣ Core Idea of Runnable (The Breakthrough)

### ✅ What is a Runnable?

> **A Runnable is a standardized unit of work that takes input and returns output using a common interface.**

At minimum, every Runnable supports:

```python
invoke(input) → output
```

Optionally:

* `batch(inputs)` → multiple outputs
* `stream(input)` → streaming output

---

## 3️⃣ Runnable Mental Model (Think Like This)

### 🧱 Lego Analogy (Very Important)

| Concept            | Runnable Meaning          |
| ------------------ | ------------------------- |
| Single Lego block  | One Runnable              |
| Same connector     | Same interface (`invoke`) |
| Combine blocks     | Compose Runnables         |
| Big Lego structure | Complex AI workflow       |

👉 **Any composition of Runnables is itself a Runnable**

---

## 4️⃣ Runnable Interface (Conceptual)

```python
class Runnable:
    def invoke(self, input):
        raise NotImplementedError
```

Everything in LangChain eventually becomes a Runnable:

* PromptTemplate → Runnable
* LLM → Runnable
* Retriever → Runnable
* OutputParser → Runnable

---

## 5️⃣ Chains vs Runnables (Key Difference)

| Chains (Old)         | Runnables (New)        |
| -------------------- | ---------------------- |
| Many special classes | Few generic primitives |
| Hard to extend       | Easy to compose        |
| Fixed workflows      | Flexible workflows     |
| Glue code needed     | No glue code           |

👉 **Chains are now just compositions of Runnables**

---

## 6️⃣ Two Types of Runnables

### 1️⃣ Task-Specific Runnables

These *do actual AI work*.

Examples:

* PromptTemplate
* ChatOpenAI
* Retriever
* OutputParser

### 2️⃣ Runnable Primitives (Most Important)

These *control execution flow*.

They decide:

* order
* parallelism
* conditions
* custom logic

---

## 7️⃣ RunnableSequence (Sequential Flow)

### 🔹 What it does

Passes output of one Runnable as input to the next.

### 🔹 Visual Flow

```
Input
 ↓
Prompt
 ↓
LLM
 ↓
Parser
 ↓
Output
```

### 🔹 Code (Basic)

```python
from langchain.schema.runnable import RunnableSequence

chain = RunnableSequence(
    prompt,
    llm,
    parser
)

result = chain.invoke({"topic": "AI"})
```

### 🔹 Using LCEL (Recommended)

```python
chain = prompt | llm | parser
```

✅ Cleaner
✅ More readable
✅ Same behavior

---

## 8️⃣ RunnableParallel (Parallel Execution)

### 🔹 What it does

Runs **multiple Runnables at the same time** with the **same input**.

### 🔹 Visual Flow

```
            ┌── Tweet Generator
Input ──────┼── LinkedIn Generator
            └── Blog Generator
```

### 🔹 Output Shape

```python
{
  "tweet": "...",
  "linkedin": "...",
  "blog": "..."
}
```

### 🔹 Code Example

```python
from langchain.schema.runnable import RunnableParallel

parallel = RunnableParallel({
    "tweet": tweet_chain,
    "linkedin": linkedin_chain
})

parallel.invoke({"topic": "LangChain"})
```

📌 **Used heavily in content generation & analytics**

---

## 9️⃣ RunnablePassThrough (Identity Runnable)

### 🔹 What it does

Returns input **unchanged**.

### 🔹 Why it exists

To **keep data alive** in complex workflows.

### 🔹 Example

```
Input Joke
 ├── Explain Joke
 └── PassThrough (original joke)
```

### 🔹 Code

```python
from langchain.schema.runnable import RunnablePassthrough
```

📌 Very useful inside `RunnableParallel`

---

## 🔟 RunnableLambda (Custom Python Logic)

### 🔹 What it does

Wraps **any Python function** as a Runnable.

### 🔹 Why it matters

Not everything needs an LLM.

### 🔹 Example Use Cases

* Word count
* Text cleaning
* Metadata extraction
* Rule-based logic

### 🔹 Code

```python
from langchain.schema.runnable import RunnableLambda

word_count = RunnableLambda(lambda x: len(x.split()))
```

📌 **Best practice:**
Use Lambda for **cheap logic**, LLM for **reasoning**

---

## 1️⃣1️⃣ RunnableBranch (Conditional Logic)

### 🔹 What it does

Implements **if–else logic** in workflows.

### 🔹 Visual Flow

```
          ┌─ Summarize
Input ────┤
          └─ Return as-is
```

### 🔹 Example Condition

* If text > 500 words → summarize
* Else → return original

### 🔹 Code Concept

```python
from langchain.schema.runnable import RunnableBranch
```

📌 Used in:

* Moderation
* Routing
* Dynamic workflows
* Agent decisions

---

## 1️⃣2️⃣ LCEL (LangChain Expression Language)

### 🔹 What is LCEL?

A **declarative syntax** for building RunnableSequence.

### 🔹 Pipe Operator (`|`)

```python
chain = prompt | llm | parser
```

### 🔹 Why LCEL is Important

* Readable
* Composable
* Pythonic
* Future extensible

📌 Currently supports **sequential logic only**

---

## 1️⃣3️⃣ Composition Rule (Very Important)

> **Anything built from Runnables is itself a Runnable**

That means:

* A chain can be reused
* Nested chains work
* Large workflows stay clean

---

## 1️⃣4️⃣ Real-World Architecture Example

### RAG Pipeline Using Runnables

```
Query
 ↓
Retriever
 ↓
Prompt
 ↓
LLM
 ↓
Parser
```

All are:

* Runnable
* Swappable
* Testable

---

## 1️⃣5️⃣ Best Practices (Industry Level)

✅ Prefer **LCEL (`|`)** for sequences
✅ Use **RunnableLambda** for cheap operations
✅ Use **RunnableParallel** to reduce latency
✅ Avoid monolithic chains
✅ Treat workflows as reusable Runnables
✅ Keep logic explicit (readability > cleverness)

---

## 🔚 Final Summary

* **Runnable is the foundation of modern LangChain**
* It standardizes how components talk to each other
* Runnable primitives give you:

  * Sequential logic
  * Parallelism
  * Conditions
  * Custom logic
* LCEL makes pipelines readable and clean
* Complex GenAI systems = composition of simple Runnables
