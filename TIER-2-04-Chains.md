# TIER 2-04: Chains
## Connecting Multiple Operations

---

## What Are Chains?

A **chain** connects multiple operations together in sequence.

```
Prompt → LLM → Parser → Output
```

Each step feeds its output into the next step.

**Simple example:**
```python
# Without chains (verbose)
prompt_text = template.invoke({"topic": "AI"})
llm_output = llm.invoke(prompt_text)
final_output = parser.invoke(llm_output)

# With chains (clean)
chain = prompt | llm | parser
final_output = chain.invoke({"topic": "AI"})
```

---

## Simple Chains

### Chain 1: Prompt → LLM
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

template = ChatPromptTemplate.from_template("What is {topic}?")
llm = ChatOpenAI(model="gpt-4")

chain = template | llm
response = chain.invoke({"topic": "AI"})
print(response.content)
```

### Chain 2: Prompt → LLM → Parser
```python
from langchain_core.output_parsers import StrOutputParser

template = ChatPromptTemplate.from_template("List 3 facts about {topic}.")
llm = ChatOpenAI(model="gpt-4")
parser = StrOutputParser()

chain = template | llm | parser
facts = chain.invoke({"topic": "Python"})
print(facts)  # Clean string, not Message object
```

### Chain 3: Prompt → LLM → JSON Parser
```python
from langchain_core.output_parsers import JsonOutputParser

template = ChatPromptTemplate.from_template(
    "Extract info from: {text}\nReturn JSON with: name, age, occupation"
)
llm = ChatOpenAI(model="gpt-4")
parser = JsonOutputParser()

chain = template | llm | parser
data = chain.invoke({"text": "John Smith, 35 years old, works as a dentist"})
print(data)  # {"name": "John Smith", "age": 35, "occupation": "dentist"}
```

---

## Complex Chains (Multiple Steps)

### Multi-Step Example: Write and Review
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Step 1: Write content
writer_template = ChatPromptTemplate.from_template(
    "Write a 100-word blog post about {topic}."
)

# Step 2: Review content
reviewer_template = ChatPromptTemplate.from_template(
    "Review this blog post and give feedback:\n{blog}\n\nFeedback:"
)

llm = ChatOpenAI(model="gpt-4")

# Create the chain
writer = writer_template | llm
reviewer = reviewer_template | llm

# Use it
topic = "AI Safety"
blog = writer.invoke({"topic": topic}).content
feedback = reviewer.invoke({"blog": blog}).content

print(f"Blog:\n{blog}\n\nFeedback:\n{feedback}")
```

---

## Conditional Chains (If-Then Logic)

### Use RunnableBranch for Conditions
```python
from langchain_core.runnables import RunnableBranch
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

# Define different paths
technical_template = ChatPromptTemplate.from_template(
    "Provide technical details about {topic}."
)

simple_template = ChatPromptTemplate.from_template(
    "Explain {topic} in simple terms."
)

# Create branch
chain = RunnableBranch(
    (lambda x: x["level"] == "technical", technical_template | llm),
    (lambda x: x["level"] == "simple", simple_template | llm),
    simple_template | llm  # Default
)

response1 = chain.invoke({"topic": "AI", "level": "technical"})
response2 = chain.invoke({"topic": "AI", "level": "simple"})
```

---

## Chains with Conditional Input

### Using RunnablePassthrough and Lambda
```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

template = ChatPromptTemplate.from_messages([
    ("system", "You are helpful."),
    ("user", "{question}")
])

llm = ChatOpenAI(model="gpt-4")

# Pass through input unchanged
chain = {"question": RunnablePassthrough()} | template | llm

response = chain.invoke("What is AI?")
```

---

## Chains with Parallel Steps

### Run Multiple Operations in Parallel
```python
from langchain_core.runnables import RunnableParallel

# Define multiple processing steps
summarizer = summary_template | llm
analyzer = analysis_template | llm
translator = translation_template | llm

# Run all in parallel
parallel_chain = RunnableParallel(
    summary=summarizer,
    analysis=analyzer,
    translation=translator
)

result = parallel_chain.invoke({"text": "Some text..."})
# result has: {"summary": "...", "analysis": "...", "translation": "..."}
```

---

## Real Example: Content Pipeline

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser

llm = ChatOpenAI(model="gpt-4")

# Step 1: Generate topic ideas
idea_template = ChatPromptTemplate.from_template(
    "Generate 3 blog topics about {domain}."
)

# Step 2: Expand on a topic
expand_template = ChatPromptTemplate.from_template(
    "Write a detailed outline for: {topic}"
)

# Step 3: Write the blog
write_template = ChatPromptTemplate.from_template(
    "Write a blog post based on: {outline}"
)

# Create chain
idea_chain = idea_template | llm
expand_chain = expand_template | llm
write_chain = write_template | llm

# Use it
ideas = idea_chain.invoke({"domain": "Machine Learning"}).content
print(f"Ideas: {ideas}\n")

# Pick first idea and expand
first_idea = "Transformers in NLP"  # From ideas
outline = expand_chain.invoke({"topic": first_idea}).content
print(f"Outline: {outline}\n")

# Write the blog
blog = write_chain.invoke({"outline": outline}).content
print(f"Blog:\n{blog}")
```

---

## Chains with Memory (Conversation)

```python
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

memory = ConversationBufferMemory(return_messages=True)
llm = ChatOpenAI(model="gpt-4")

# Template with conversation history
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{question}")
])

# Chain
chain = template | llm

# First turn
response1 = chain.invoke({
    "question": "What is AI?",
    "chat_history": []
})
memory.chat_memory.add_user_message("What is AI?")
memory.chat_memory.add_ai_message(response1.content)

# Second turn (with history)
response2 = chain.invoke({
    "question": "Tell me more",
    "chat_history": memory.chat_memory.messages
})
memory.chat_memory.add_user_message("Tell me more")
memory.chat_memory.add_ai_message(response2.content)

print(response1.content)
print(response2.content)
```

---

## Chains with Error Handling

```python
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

template = ChatPromptTemplate.from_template("Explain {topic}.")
llm = ChatOpenAI(model="gpt-4")

def handle_error(e):
    return f"Error: {str(e)}. Please try again."

# Create chain with fallback
chain = template | llm

# Add error handling
safe_chain = chain.with_fallback(
    RunnableLambda(handle_error)
)

try:
    response = safe_chain.invoke({"topic": "AI"})
except Exception as e:
    response = handle_error(e)

print(response)
```

---

## Chains: Async and Streaming

### Async Chain
```python
import asyncio

async def run_async_chain():
    response = await chain.ainvoke({"topic": "AI"})
    return response.content

result = asyncio.run(run_async_chain())
print(result)
```

### Streaming Chain
```python
print("Response: ", end="", flush=True)
for chunk in chain.stream({"topic": "AI"}):
    print(chunk.content, end="", flush=True)
print()  # Newline
```

---

## Debugging Chains

### See What's Happening
```python
# Enable debug output
import logging
logging.basicConfig(level=logging.DEBUG)

chain = template | llm
response = chain.invoke({"topic": "AI"})
# See all intermediate steps
```

### Inspect Intermediate Outputs
```python
def debug_prompt(x):
    print(f"Prompt: {x}")
    return x

def debug_llm(x):
    print(f"LLM Output: {x}")
    return x

chain = (
    template
    | RunnableLambda(debug_prompt)
    | llm
    | RunnableLambda(debug_llm)
)

response = chain.invoke({"topic": "AI"})
```

---

## Real Code: Production Q&A Chain

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnableBranch

llm = ChatOpenAI(model="gpt-4")

# Route based on question type
technical_template = ChatPromptTemplate.from_template(
    "Answer this technical question: {question}"
)

general_template = ChatPromptTemplate.from_template(
    "Answer this general question: {question}"
)

# Branch logic
is_technical = lambda x: "technical" in x["question"].lower()

# Create branch
qa_chain = RunnableBranch(
    (is_technical, technical_template | llm),
    general_template | llm
)

# Use it
answer = qa_chain.invoke({"question": "What is a neural network?"})
print(answer.content)
```

---

## Self-Check

Can you answer:

- [ ] "What is a chain?" (Connected operations using pipe operator)
- [ ] "How do you create a simple chain?" (prompt | llm | parser)
- [ ] "How do you run parallel operations?" (RunnableParallel)
- [ ] "How do you add conditions to chains?" (RunnableBranch)
- [ ] "How do you handle errors?" (with_fallback)

Ready for **[TIER-2-05-Embeddings-Explained.md](TIER-2-05-Embeddings-Explained.md)** →

Next: Converting text to vectors for semantic search.
