# 🧠 LangChain Prompts (Code + Concepts)

This repository provides **end-to-end, production-style code examples** for understanding **Prompts in GenAI using LangChain**.

The goal is simple:

> Learn prompts **step-by-step**, from **basic static prompts** to **advanced chatbots with history and dynamic templates**.

---

## 1️⃣ Basic Static Prompt (No Template)

### Problem

A simple one-time prompt without reusability or validation.

```python
from langchain_openai import OpenAI

llm = OpenAI(temperature=0)

response = llm.invoke("Explain Machine Learning in simple words")
print(response)
```

❌ Not scalable
❌ No structure

---

## 2️⃣ Understanding Temperature

```python
from langchain_openai import OpenAI

llm_low = OpenAI(temperature=0)
llm_high = OpenAI(temperature=1.2)

prompt = "Write a short story about a robot"

print(llm_low.invoke(prompt))
print(llm_high.invoke(prompt))
```

✔ Low temperature → deterministic
✔ High temperature → creative

---

## 3️⃣ Dynamic Prompt using PromptTemplate

### Why PromptTemplate?

* Validation
* Reusability
* Clean design

```python
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI

llm = OpenAI(temperature=0)

prompt_template = PromptTemplate(
    input_variables=["topic", "tone", "length"],
    template="Explain {topic} in a {tone} manner in {length} words."
)

prompt = prompt_template.format(
    topic="Docker",
    tone="simple",
    length="100"
)

print(llm.invoke(prompt))
```

---

## 4️⃣ PromptTemplate + Chain (Best Practice)

```python
from langchain.chains import LLMChain
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

llm = OpenAI(temperature=0)

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} for beginners"
)

chain = LLMChain(llm=llm, prompt=prompt)

print(chain.invoke({"topic": "Kubernetes"}))
```

✔ Cleaner
✔ Maintainable

---

## 5️⃣ Simple Chatbot (Without Memory)

```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

chat = ChatOpenAI(temperature=0)

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    response = chat.invoke([HumanMessage(content=user_input)])
    print("AI:", response.content)
```

❌ No context
❌ No memory

---

## 6️⃣ Chat History using Normal Python List

```python
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

chat = ChatOpenAI(temperature=0)
chat_history = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    chat_history.append(HumanMessage(content=user_input))
    response = chat.invoke(chat_history)
    chat_history.append(AIMessage(content=response.content))

    print("AI:", response.content)
```

✔ Context preserved

---

## 7️⃣ Adding SystemMessage (Role Definition)

```python
from langchain.schema import SystemMessage

chat_history = [
    SystemMessage(content="You are a helpful AI tutor who explains things simply")
]
```

SystemMessage is always added **once at the beginning**.

---

## 8️⃣ ChatPromptTemplate (Dynamic Multi-Message Prompt)

```python
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert {role}"),
    ("human", "Explain {topic} in simple words")
])

messages = prompt.format_messages(
    role="Backend Engineer",
    topic="Microservices"
)

response = chat.invoke(messages)
print(response.content)
```

✔ Fully dynamic
✔ Structured chat prompts

---

## 9️⃣ MessagePlaceholder (Advanced Chat History Handling)

### Problem

Manual history handling becomes messy at scale.

### Solution

Use `MessagePlaceholder`.

```python
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful customer support assistant"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{query}")
])

chat_history = [
    HumanMessage(content="I want a refund"),
    AIMessage(content="Sure, can you share your order ID?")
]

messages = prompt.format_messages(
    chat_history=chat_history,
    query="Here is my order id 123"
)

response = chat.invoke(messages)
print(response.content)
```

✔ Clean
✔ Scalable
✔ Production ready

---

## 🔟 Real-World Chatbot Flow

1. Store chat history in DB / file
2. Load history
3. Inject using MessagePlaceholder
4. Invoke model
5. Append response

This is how **ChatGPT-like systems** work.
