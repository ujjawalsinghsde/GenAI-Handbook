# 📘 Structured Output in LangChain

## 🧠 1. What Is Structured Output?

When an LLM responds with raw text, it is called **unstructured output**. This is easy for humans but hard for code to interpret reliably.

**Structured output** means the model returns data in a **strict format** (like JSON or typed objects), so your code can use it directly without error-prone string parsing.

---

## 🧩 2. Why Structured Output Matters

Structured output unlocks true application building with LLMs:

| Advantage          | Impact                                      |
| ------------------ | ------------------------------------------- |
| Easy to parse      | No manual regex or text extraction          |
| Reliable           | Models are forced into a predictable format |
| Faster integration | Works directly with APIs/DBs                |
| Better for agents  | Agents depend on predictable outputs        |

In short: **structured output bridges LLMs with real systems**.

---

## 🛠 3. Core Methods for Structured Output in LangChain

LangChain provides utilities to receive structured data from the model using:

1. **TypedDict**
2. **Pydantic Models**
3. **JSON Schema**

You will see code for all three approaches.

---

## 🧠 4. Common Workflow

1. Define the schema (TypedDict / Pydantic / JSON)
2. Attach it to an LLM using `.with_structured_output()`
3. Give the input text
4. Receive the structured data

```python
response = structured_llm.invoke(input_text)
print(response)
```

This `response` is already structured, validated, and ready to use.

---

## 🧰 5. Code Examples (Copied From Repo Structure)

## 5.1 🔹 TypedDict Example

> *Simple Python dictionary type with type hints.*

```python
from typing import TypedDict
from langchain import OpenAI

class StudentOutput(TypedDict):
    name: str
    roll: int
    cgpa: float

llm = OpenAI(model="gpt-4o-mini")
structured_llm = llm.with_structured_output(StudentOutput)

prompt = "Extract student info from: John Doe, roll 24, CGPA 8.7"

result = structured_llm.invoke(prompt)
print(result)  # {'name': 'John Doe', 'roll': 24, 'cgpa': 8.7}
```

⚠️ **Note**: TypedDict *does not validate* types — it only hints them. If the model returns wrong types, your code may crash later.

Use this for **prototyping and learning**.
---

## 5.2 🔹 Pydantic Example

> *Validated and type-safe data models.*

```python
from pydantic import BaseModel, Field
from langchain import OpenAI

class Student(BaseModel):
    name: str = Field(description="Name of student")
    roll: int = Field(description="Roll number")
    cgpa: float = Field(ge=0.0, le=10.0)

llm = OpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(Student)

prompt = "Student: Arjun, roll 101, CGPA 9.2"

response = structured_llm.invoke(prompt)
print(response.dict())
```

**Benefits of Pydantic:**

* Automatically **validates types**
* Enforces constraints (`ge`, `le`)
* Easy `.dict()`/ `.json()` conversion

This is **ideal for production** code.

---

## 5.3 🔹 JSON Schema Example

> *Language-agnostic structured output*

```python
from langchain import OpenAI


# schema
json_schema = {
  "title": "Review",
  "type": "object",
  "properties": {
    "key_themes": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Write down all the key themes discussed in the review in a list"
    },
    "summary": {
      "type": "string",
      "description": "A brief summary of the review"
    },
    "sentiment": {
      "type": "string",
      "enum": ["pos", "neg"],
      "description": "Return sentiment of the review either negative, positive or neutral"
    },
    "pros": {
      "type": ["array", "null"],
      "items": {
        "type": "string"
      },
      "description": "Write down all the pros inside a list"
    },
    "cons": {
      "type": ["array", "null"],
      "items": {
        "type": "string"
      },
      "description": "Write down all the cons inside a list"
    },
    "name": {
      "type": ["string", "null"],
      "description": "Write the name of the reviewer"
    }
  },
  "required": ["key_themes", "summary", "sentiment"]
}

llm = OpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(json_schema)

prompt = "Review: The battery life is good, but the camera quality is average."
result = structured_llm.invoke(prompt)
print(result)
```

Use JSON Schema when you want structured data that’s **platform-agnostic** (frontend ↔ backend systems).

---

## 🧠 6. Parsing and Usage

After invoking the model:

```python
print(result["sentiment"])
```

You can directly:

* Store in database
* Send as API JSON response
* Feed into agent pipelines

No messy manual text extraction.

---

## 🧪 7. When to Choose Which Schema

| Schema      | Strict Validation | Best Use Case                |
| ----------- | ----------------- | ---------------------------- |
| TypedDict   | ❌                 | Quick prototyping            |
| Pydantic    | ✅                 | Production systems           |
| JSON Schema | ❌*                | Cross-platform data exchange |

* JSON Schema *ensures format*, but doesn’t coerce to strict Python types.

---

## 🧠 8. What Happens Internally

When you call:

```python
model.with_structured_output(schema)
```

LangChain:

1. Adds **instructions** to the prompt telling the model the schema.
2. Parses model output into the target format.
3. Returns a **structured object** (dict or model instance).

This saves manual prompt engineering and parsing code.

---

## 🧠 9. Agent Integration (Advanced)

Structured output becomes essential when building **agents that use tools** or interact with external APIs.

LangChain’s agents automatically decide between:

* **Native structured support** (when model supports it)
* **Tool-calling fallback**

This is beyond basic models — but the principle is the same:
➡ structured data = predictable downstream behavior.

---

## 🧠 10. Limitations & Gotchas

1. Some **open-source models** do not natively support structured output → you’ll need output parsers (covered later).
2. TypedDict won’t catch wrong types
3. Always validate critical data before usage

---

## 🧠 11. Summary

Structured output turns LLMs from **chat interfaces** into **real application components**:

✅ Predictable format
✅ Self-validating data
✅ Easy integration with systems
✅ Foundation for agents & APIs
