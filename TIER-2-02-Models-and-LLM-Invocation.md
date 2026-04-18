# TIER 2-02: Models and LLM Invocation
## Calling LLMs Through LangChain

---

## The Simple Way: Calling an LLM

Before LangChain (raw API):
```python
import openai

openai.api_key = "sk-..."
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response['choices'][0]['message']['content'])
```

With LangChain (clean):
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
response = llm.invoke("Hello")
print(response.content)
```

**That's much cleaner.**

---

## Supported Models in LangChain

### OpenAI Models
```python
from langchain_openai import ChatOpenAI

# GPT-4 (most capable)
gpt4 = ChatOpenAI(model="gpt-4")

# GPT-4 Turbo (cheaper, faster)
gpt4_turbo = ChatOpenAI(model="gpt-4-turbo-preview")

# GPT-3.5 Turbo (cheapest)
gpt35 = ChatOpenAI(model="gpt-3.5-turbo")
```

### Anthropic (Claude)
```python
from langchain_anthropic import ChatAnthropic

# Claude 3 Opus (most capable)
claude_opus = ChatAnthropic(model="claude-3-opus-20240229")

# Claude 3 Sonnet (balanced)
claude_sonnet = ChatAnthropic(model="claude-3-sonnet-20240229")

# Claude 3 Haiku (cheapest, fastest)
claude_haiku = ChatAnthropic(model="claude-3-haiku-20240307")
```

### Google Gemini
```python
from langchain_google_genai import ChatGoogleGenerativeAI

gemini = ChatGoogleGenerativeAI(model="gemini-pro")
```

### Open Source Models (via Ollama/Hugging Face)
```python
from langchain_community.llms import Ollama

# Run locally
llm = Ollama(model="llama2")

# Or from Hugging Face
from langchain_huggingface import HuggingFaceHub
llm = HuggingFaceHub(repo_id="meta-llama/Llama-2-7b")
```

---

## Initialization: Setting Up Models

### Method 1: Direct Parameters
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4",
    api_key="your-key-here",
    temperature=0.7,
    max_tokens=500
)
```

### Method 2: Environment Variables (Better)
```bash
# In your .env file or shell
export OPENAI_API_KEY="sk-..."
```

```python
from langchain_openai import ChatOpenAI

# Auto-reads from environment
llm = ChatOpenAI(model="gpt-4")
```

**Benefit:** Don't hardcode API keys in code.

### Method 3: With Full Configuration
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.2,           # Low = deterministic
    max_tokens=1000,           # Output length
    top_p=0.9,                 # Nucleus sampling
    frequency_penalty=0.5,     # Reduce repetition
    request_timeout=60,        # Timeout seconds
    max_retries=3              # Auto-retry on failure
)
```

---

## Invoking Models (Different Methods)

### Method 1: `.invoke()` - Simple, Wait for Full Response
```python
response = llm.invoke("What is AI?")
print(response.content)

# Blocks until full response is ready
# Use for: Batch processing, when you need full response
```

### Method 2: `.stream()` - Get Response Token by Token
```python
for chunk in llm.stream("What is AI?"):
    print(chunk.content, end="", flush=True)

# Prints tokens as they're generated
# Use for: Real-time UI, responsive feel, long responses
```

### Method 3: `.batch()` - Process Multiple Inputs
```python
prompts = [
    "What is AI?",
    "What is ML?",
    "What is DL?"
]

responses = llm.batch(prompts)
for response in responses:
    print(response.content)

# More efficient than calling invoke 3 times
# Use for: Batch processing multiple requests
```

### Method 4: `.ainvoke()` - Async (Non-blocking)
```python
import asyncio

async def get_response():
    response = await llm.ainvoke("What is AI?")
    return response.content

result = asyncio.run(get_response())
print(result)

# Non-blocking, allows other code to run
# Use for: Web servers, concurrent requests
```

---

## Message Formats

LLMs expect structured messages with roles:

### Format 1: Simple String
```python
response = llm.invoke("What is AI?")
# Simple but limited
```

### Format 2: List of Messages
```python
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is AI?"),
    AIMessage(content="AI is..."),
    HumanMessage(content="Tell me more.")
]

response = llm.invoke(messages)
```

### Format 3: With ChatPromptTemplate (Better)
```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {domain}."),
    ("user", "Explain {topic}.")
])

messages = prompt.invoke({"domain": "physics", "topic": "quantum mechanics"})
response = llm.invoke(messages)
```

---

## Handling Responses

### Response Objects
Every response is a Message object:

```python
response = llm.invoke("What is AI?")

# Access content
print(response.content)  # "AI is..."

# Access metadata
print(response.type)     # "ai"
print(response.metadata) # {"tokencount": 45, ...}

# For streaming, chunk by chunk
for chunk in llm.stream("What is AI?"):
    print(chunk.content, end="")
    print(f" [tokens: {len(chunk.content.split())}]")
```

---

## Model Parameters and What They Do

### Temperature
```python
# Deterministic (always same output)
llm_det = ChatOpenAI(model="gpt-4", temperature=0)

# Normal randomness
llm_normal = ChatOpenAI(model="gpt-4", temperature=0.7)

# Very creative
llm_creative = ChatOpenAI(model="gpt-4", temperature=1.5)
```

### Max Tokens
```python
# Short responses
llm_short = ChatOpenAI(model="gpt-4", max_tokens=50)

# Long responses
llm_long = ChatOpenAI(model="gpt-4", max_tokens=2000)

# Use what you need to control costs
```

### Top P
```python
# Only top 50% of tokens
llm_focused = ChatOpenAI(model="gpt-4", top_p=0.5)

# All tokens (normal)
llm_normal = ChatOpenAI(model="gpt-4", top_p=1.0)
```

### Frequency Penalty
```python
# Reduce repetition
llm_diverse = ChatOpenAI(model="gpt-4", frequency_penalty=0.5)

# Allow repetition
llm_normal = ChatOpenAI(model="gpt-4", frequency_penalty=0)
```

---

## Error Handling

### Handle Rate Limits
```python
from langchain_core.exceptions import RateLimitError
import time

def call_with_retry(llm, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return llm.invoke(prompt)
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

response = call_with_retry(llm, "What is AI?")
```

### Handle API Errors
```python
from langchain_core.exceptions import APIConnectionError

try:
    response = llm.invoke("What is AI?")
except APIConnectionError:
    print("API connection failed")
except Exception as e:
    print(f"Error: {e}")
```

---

## Token Counting

Know how many tokens you're using:

```python
# For OpenAI models
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

# Count tokens in a string
text = "What is artificial intelligence?"
token_count = llm.get_num_tokens(text)
print(f"Tokens: {token_count}")

# Count tokens in messages
from langchain_core.messages import HumanMessage

messages = [HumanMessage(content="What is AI?")]
token_count = llm.get_num_tokens_from_messages(messages)
print(f"Tokens: {token_count}")
```

**Why it matters:** Different models have different token limits and costs.

---

## Practical Example: Multi-Model Comparison

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

def compare_models(prompt):
    models = {
        "GPT-4": ChatOpenAI(model="gpt-4", temperature=0.7),
        "Claude Opus": ChatAnthropic(model="claude-3-opus-20240229"),
        "GPT-3.5": ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
    }
    
    for name, llm in models.items():
        print(f"\n{name}:")
        response = llm.invoke(prompt)
        print(response.content[:200] + "...")  # First 200 chars

compare_models("Explain quantum computing")
```

**Benefit:** Easy to test different models.

---

## Choosing the Right Model

### For Most Tasks: Claude 3 Sonnet
- Great quality
- Reasonable price
- Fast inference
- 200K context window

### For Maximum Quality: GPT-4
- Best reasoning
- Best code generation
- Most expensive
- Slower inference

### For Budget: GPT-3.5 Turbo or Claude 3 Haiku
- Good enough for many tasks
- 1/10th the price of GPT-4
- Fast
- Sufficient context

### For Local/Private: Llama 2 or Mistral
- Run on your own hardware
- No API costs
- Full privacy
- Slightly lower quality

---

## Best Practices

### 1. Use Environment Variables
```python
import os

api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4", api_key=api_key)
```

### 2. Set Appropriate Timeouts
```python
llm = ChatOpenAI(
    model="gpt-4",
    request_timeout=30,  # 30 seconds
    max_retries=3        # Auto-retry
)
```

### 3. Use Async for Concurrent Requests
```python
async def process_batch(prompts):
    tasks = [llm.ainvoke(p) for p in prompts]
    results = await asyncio.gather(*tasks)
    return results
```

### 4. Monitor Token Usage
```python
for model_name, llm in models.items():
    tokens = llm.get_num_tokens(prompt)
    cost = tokens * PRICE_PER_TOKEN
    print(f"{model_name}: {tokens} tokens (${cost:.4f})")
```

### 5. Handle Streaming for UX
```python
print("Response: ", end="", flush=True)
for chunk in llm.stream(prompt):
    print(chunk.content, end="", flush=True)
print()  # Newline at end
```

---

## Real-World Code: LLM Selection Based on Task

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

def get_llm_for_task(task_type):
    if task_type == "reasoning":
        # Complex reasoning needs best model
        return ChatOpenAI(model="gpt-4", temperature=0.2)
    
    elif task_type == "creative":
        # Creative needs variety
        return ChatAnthropic(model="claude-3-sonnet", temperature=1.0)
    
    elif task_type == "budget":
        # Budget-conscious
        return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    
    else:
        # Default: balanced
        return ChatAnthropic(model="claude-3-sonnet", temperature=0.7)

# Usage
llm = get_llm_for_task("reasoning")
response = llm.invoke("Explain quantum entanglement")
```

---

## Self-Check

Can you answer:

- [ ] "How do you initialize a ChatOpenAI model?" (ChatOpenAI(model="gpt-4"))
- [ ] "What's the difference between invoke and stream?" (invoke waits for full response; stream gives tokens as they come)
- [ ] "How do you handle rate limiting?" (Retry with exponential backoff)
- [ ] "Why use environment variables for API keys?" (Security, don't hardcode secrets)
- [ ] "How do you count tokens?" (llm.get_num_tokens(text))

Ready for **[TIER-2-03-Prompts-and-Templates.md](TIER-2-03-Prompts-and-Templates.md)** →

Next: Reusable prompt templates.
