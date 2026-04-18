# TIER 2-03: Prompts and Templates
## Reusable, Parameterized Prompts

---

## The Problem: Repeating Prompts

Without templates:
```python
# Manual string concatenation
topic = "quantum computing"
audience = "5th grader"

prompt1 = f"Explain {topic} to a {audience}"
response1 = llm.invoke(prompt1)

topic2 = "machine learning"
audience2 = "software engineer"

prompt2 = f"Explain {topic2} to a {audience2}"
response2 = llm.invoke(prompt2)

# Repetitive and error-prone
```

With templates:
```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "Explain {topic} to a {audience}."
)

prompt1 = template.invoke({"topic": "quantum computing", "audience": "5th grader"})
response1 = llm.invoke(prompt1)

prompt2 = template.invoke({"topic": "machine learning", "audience": "software engineer"})
response2 = llm.invoke(prompt2)

# Reusable, clean
```

---

## Simple Prompt Templates

### Method 1: Basic Template
```python
from langchain_core.prompts import PromptTemplate

template = PromptTemplate.from_template(
    "What is {subject}?"
)

# Use it
prompt = template.invoke({"subject": "AI"})
print(prompt)  # Output: "What is AI?"

response = llm.invoke(prompt)
```

### Method 2: Multiple Variables
```python
template = PromptTemplate.from_template(
    "Explain {topic} to a {audience} in {language}."
)

prompt = template.invoke({
    "topic": "quantum mechanics",
    "audience": "high school student",
    "language": "simple English"
})

response = llm.invoke(prompt)
```

### Method 3: With Validation
```python
template = PromptTemplate(
    input_variables=["topic", "audience"],
    template="Explain {topic} to a {audience}."
)

# This validates variables
prompt = template.invoke({"topic": "AI", "audience": "expert"})
```

---

## Chat Prompt Templates (System + User Messages)

### Method 1: From Messages List
```python
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {domain}."),
    ("user", "Explain {concept} in {language}.")
])

prompt = template.invoke({
    "domain": "physics",
    "concept": "quantum entanglement",
    "language": "simple terms"
})

response = llm.invoke(prompt)
```

### Method 2: Multiple System Messages
```python
template = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}."),
    ("system", "Your tone is {tone}."),
    ("user", "{question}?")
])

prompt = template.invoke({
    "role": "friendly teacher",
    "tone": "encouraging and warm",
    "question": "What is machine learning"
})
```

### Method 3: Mixed Format
```python
from langchain_core.messages import SystemMessage, HumanMessagePromptTemplate

template = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful assistant."),
    HumanMessagePromptTemplate.from_template("{user_input}")
])

prompt = template.invoke({"user_input": "Hello!"})
```

---

## Advanced: Conditional Prompts

### Based on User Input
```python
from langchain_core.prompts import ChatPromptTemplate

def get_template(complexity):
    if complexity == "simple":
        return ChatPromptTemplate.from_messages([
            ("system", "Explain in very simple terms."),
            ("user", "{question}")
        ])
    else:
        return ChatPromptTemplate.from_messages([
            ("system", "Provide a technical, detailed explanation."),
            ("user", "{question}")
        ])

template = get_template("simple")
prompt = template.invoke({"question": "What is AI?"})
response = llm.invoke(prompt)
```

---

## Real Example: Multi-Purpose Translator

```python
from langchain_core.prompts import ChatPromptTemplate

# One template for multiple languages
translator = ChatPromptTemplate.from_messages([
    ("system", "You are a translator. Translate to {target_language} only."),
    ("user", "{text}")
])

# Translate to Spanish
spanish = translator.invoke({
    "target_language": "Spanish",
    "text": "Hello, how are you?"
})
print(llm.invoke(spanish).content)  # "Hola, ¿cómo estás?"

# Translate to French
french = translator.invoke({
    "target_language": "French",
    "text": "Hello, how are you?"
})
print(llm.invoke(french).content)  # "Bonjour, comment allez-vous?"
```

---

## Prompt Templates with LLM Calls (Chains)

### Method 1: Simple Chain
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms."
)

llm = ChatOpenAI(model="gpt-4")

# Create a chain: prompt → LLM
chain = prompt | llm

response = chain.invoke({"topic": "quantum computing"})
print(response.content)
```

### Method 2: With Output Parser
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template(
    "List 3 facts about {topic}."
)

llm = ChatOpenAI(model="gpt-4")
parser = StrOutputParser()

# Chain: prompt → LLM → parse output
chain = prompt | llm | parser

facts = chain.invoke({"topic": "Python"})
print(facts)  # Clean string, not Message object
```

---

## Dynamic Prompts: Using Retrieval

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

template = ChatPromptTemplate.from_messages([
    ("system", "Use the context to answer the question."),
    ("system", "Context: {context}"),
    ("user", "{question}")
])

# Chain with context from retriever
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | template
    | llm
)

answer = chain.invoke("What is in the documents?")
```

---

## Few-Shot Prompts: Learning by Example

### With Examples
```python
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate

# Define examples
examples = [
    {"input": "What is AI?", "output": "AI is artificial intelligence."},
    {"input": "What is ML?", "output": "ML is machine learning."},
]

# Define format for each example
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Q: {input}\nA: {output}"
)

# Create few-shot template
few_shot = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="Q: {question}\nA: ",
    input_variables=["question"]
)

prompt_text = few_shot.format(question="What is DL?")
print(prompt_text)

# Output:
# Q: What is AI?
# A: AI is artificial intelligence.
#
# Q: What is ML?
# A: ML is machine learning.
#
# Q: What is DL?
# A:
```

---

## Practical Example: Resume Parser

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

# Template
parser = JsonOutputParser()

template = ChatPromptTemplate.from_template(
    """Extract information from this resume:

{resume_text}

Return JSON with keys: name, email, phone, skills, experience_years"""
)

llm = ChatOpenAI(model="gpt-4")

# Chain
chain = template | llm | parser

# Use it
resume = """
John Doe | john@email.com | 555-1234
Senior Python Developer with 8 years of experience.
Skills: Python, JavaScript, React, AWS
"""

result = chain.invoke({"resume_text": resume})
print(result)
# Output: {"name": "John Doe", "email": "john@email.com", ...}
```

---

## Template Debugging

### See What Template Produces
```python
template = ChatPromptTemplate.from_template(
    "Explain {topic} to a {audience}."
)

# See the actual prompt
prompt_value = template.invoke({"topic": "AI", "audience": "beginner"})
print(prompt_value)  # See formatted prompt before sending to LLM
```

### Validate Template
```python
# Catch missing variables early
template = ChatPromptTemplate.from_template(
    "Explain {topic} to a {audience}."
)

try:
    # Missing 'audience'
    prompt = template.invoke({"topic": "AI"})
except KeyError as e:
    print(f"Missing variable: {e}")
```

---

## Best Practices

### 1. Store Templates in Files or Config
```python
TEMPLATES = {
    "translate": "Translate to {language}: {text}",
    "summarize": "Summarize in {num_sentences} sentences: {text}",
    "explain": "Explain {topic} to a {audience}."
}

template = ChatPromptTemplate.from_template(TEMPLATES["translate"])
```

### 2. Version Your Prompts
```python
SYSTEM_PROMPT_V1 = "You are helpful."
SYSTEM_PROMPT_V2 = "You are helpful, honest, and harmless."

template_v2 = ChatPromptTemplate.from_template(
    f"System: {SYSTEM_PROMPT_V2}\nUser: {{question}}"
)
```

### 3. Use Clear Variable Names
```python
# ✅ Good
"Translate to {target_language}: {source_text}"

# ❌ Bad
"Translate to {a}: {b}"
```

### 4. Document Templates
```python
template = ChatPromptTemplate.from_template(
    """Explain {topic} to a {audience}.
    
    This template is for educational explanations.
    - topic: the subject to explain
    - audience: the target audience (e.g., "5th grader", "expert")
    """
)
```

---

## Self-Check

Can you answer:

- [ ] "What's the benefit of templates?" (Reusability, clean code)
- [ ] "How do you create a simple template?" (PromptTemplate.from_template())
- [ ] "How do you chain prompt → LLM?" (prompt | llm)
- [ ] "What are few-shot prompts?" (Provide examples before asking the question)
- [ ] "How do you use templates with output parsers?" (prompt | llm | parser)

Ready for **[TIER-2-04-Chains.md](TIER-2-04-Chains.md)** →

Next: Connecting multiple operations together.
