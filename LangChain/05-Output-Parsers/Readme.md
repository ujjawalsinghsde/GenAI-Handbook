# Output Parsers in LangChain

## Why Output Parsers Exist

Large Language Models excel at text generation, but applications require structured data formats. Raw LLM output is qualitatively better for human readability but unsuitable for programmatic use.

* JSON for APIs
* Dicts for business logic
* Typed objects for validation
* Lists for iteration
* Clean strings without metadata

### ❌ Problem with Raw LLM Output

```text
"Sure! Here are the details you asked for:
Name: Rahul
Age: Twenty Five
City: Bangalore"
```

This looks fine to humans ❌
But machines can’t safely:

* Store this in DB
* Validate age
* Call APIs
* Apply business rules

👉 **Output Parsers solve this gap**

---

## 2️⃣ What is an Output Parser in LangChain?

An **Output Parser** is a component in LangChain that:

> Converts **raw LLM text output** into a **structured, predictable, and usable format**

Think of it as:

```
LLM Output  ──► Output Parser ──► Clean Structured Data
```

---

## 3️⃣ Where Output Parsers Fit in LangChain Architecture

```text
PromptTemplate
      ↓
     LLM
      ↓
 OutputParser
      ↓
 Application Logic (DB, API, UI, etc.)
```

Without an Output Parser → fragile system
With Output Parser → **production-ready system**

---

## 4️⃣ Types of Output Parsers (From Simple → Strict)

LangChain provides multiple parsers. We’ll move **from beginner to advanced**, exactly how you should learn.

---

# 🟢 1. String Output Parser (Beginner Level)

### 🎯 Purpose

Extract **only the text** from the LLM response.

### ❓ Why Needed?

LLMs return objects like:

```python
AIMessage(content="...", metadata={...})
```

You usually want:

```text
"..."
```

### ✅ When to Use

* Summaries
* Explanations
* Blog generation
* Chaining LLM outputs

---

### 🔹 Example: StringOutputParser

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = PromptTemplate(
    template="Explain {topic} in simple words",
    input_variables=["topic"]
)

chain = prompt | llm | StrOutputParser()

result = chain.invoke({"topic": "Output Parsers in LangChain"})
print(result)
```

### 🧠 Key Learning

* Removes metadata
* Clean chaining
* No structure, no validation

---

# 🟡 2. JSON Output Parser (Basic Structured Output)

### 🎯 Purpose

Force the LLM to return **JSON format**

### ❗ Important Limitation

* JSON **structure is not enforced**
* LLM decides keys

---

### 🔹 Example: JsonOutputParser

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import JsonOutputParser

parser = JsonOutputParser()

prompt = PromptTemplate(
    template="""
    Give details about a person.
    {format_instructions}
    """,
    input_variables=[],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

llm = ChatOpenAI(model="gpt-4o-mini")

chain = prompt | llm | parser

result = chain.invoke({})
print(result)
```

### 🧠 Output

```python
{
  "name": "Amit",
  "age": 25,
  "city": "Delhi"
}
```

### ⚠️ Risk

Tomorrow the model may return:

```json
{"person_name": "...", "years": "..."}
```

---

# 🟠 3. Structured Output Parser (Schema Control)

### 🎯 Purpose

Force **fixed JSON keys**

### ❗ Limitation

* No data type validation
* Values may still be wrong

---

### 🔹 Define Response Schema

```python
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

schemas = [
    ResponseSchema(name="name", description="Person name"),
    ResponseSchema(name="age", description="Person age"),
    ResponseSchema(name="city", description="City name")
]

parser = StructuredOutputParser.from_response_schemas(schemas)
```

---

### 🔹 Use with Prompt

```python
prompt = PromptTemplate(
    template="""
    Provide person details.
    {format_instructions}
    """,
    input_variables=[],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

chain = prompt | llm | parser
result = chain.invoke({})
print(result)
```

### 🧠 Output (Guaranteed Keys)

```python
{
  "name": "Rohit",
  "age": "twenty five",
  "city": "Mumbai"
}
```

❌ Age is still wrong type

---

# 🔴 4. Pydantic Output Parser (Production-Grade)

### 🎯 Purpose

* Schema enforcement
* Type validation
* Constraints
* Safe for APIs & DBs

This is what you should use in **real systems**.

---

## 🔹 Define Pydantic Model

```python
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

class Person(BaseModel):
    name: str = Field(description="Name of the person")
    age: int = Field(gt=18, description="Age must be greater than 18")
    city: str = Field(description="City name")
```

---

## 🔹 Create Parser & Chain

```python
parser = PydanticOutputParser(pydantic_object=Person)

prompt = PromptTemplate(
    template="""
    Generate valid person data.
    {format_instructions}
    """,
    input_variables=[],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

chain = prompt | llm | parser
result = chain.invoke({})
print(result)
```

---

### 🧠 Output (Typed Object)

```python
Person(
  name='Ankit',
  age=26,
  city='Pune'
)
```

### 🚀 Benefits

* Type safety
* Automatic validation
* Ideal for APIs, DB, ML pipelines

---

## 5️⃣ Comparison Summary (Exam + Interview Ready)

| Parser                 | Structure      | Validation | Use Case           |
| ---------------------- | -------------- | ---------- | ------------------ |
| StringOutputParser     | ❌              | ❌          | Plain text         |
| JsonOutputParser       | ✅              | ❌          | Quick JSON         |
| StructuredOutputParser | ✅ (Fixed Keys) | ❌          | Controlled JSON    |
| PydanticOutputParser   | ✅              | ✅          | Production systems |

---

## 6️⃣ Best Practices (From Experience)

✅ Use **StringOutputParser** for chaining LLMs
✅ Use **PydanticOutputParser** for APIs & DB
❌ Never trust raw LLM text
❌ Don’t use JSON parser for strict workflows
✅ Always validate external LLM data

---

## 7️⃣ Mental Model to Remember

> **Prompt controls what the model says**
> **Parser controls what your system accepts**

