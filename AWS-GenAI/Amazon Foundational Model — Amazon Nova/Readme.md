# 📘 **Amazon Foundational Model — Amazon Nova**

Amazon Nova is Amazon’s new family of advanced **Foundation Models (FMs)** available through **Amazon Bedrock**.
These models are designed to give developers high-performance **multimodal**, **reasoning**, and **tool-calling** capabilities at enterprise scale.

---

# 1️⃣ **Amazon Nova — Family of Foundation Models**

Amazon Nova is Amazon’s **latest generation of foundation models** designed to compete with GPT-4, Claude 3.5, Mistral, Gemini, etc.

Nova models come in three main variants:

---

## ⭐ **1. Amazon Nova Pro**

* Most powerful model in Nova family
* High reasoning capability
* Best for:

  * Agents
  * Knowledge assistants
  * Advanced chatbots
  * Complex enterprise use-cases

Think of it as **Amazon’s GPT-4+ equivalent**.

---

## ⭐ **2. Amazon Nova Lite**

* Smaller, more cost-effective
* Good for:

  * Fast responses
  * Lightweight reasoning
  * Low-latency chatbots
  * High-volume applications

Think of it as **GPT-3.5 Turbo equivalent**, but better optimized.

---

## ⭐ **3. Amazon Nova Micro**

* Tiny and ultra-fast
* Great for:

  * Autocomplete
  * Simple classification
  * On-device or low-cost apps
  * Quick suggestions

Equivalent mindset: **A tiny LLM for fast tasks**.

---

## 🔍 **Common Features Across Nova Models**

* Multimodal (text + images + video)
* Low hallucination rate
* Efficient and scalable
* Natively optimized for Bedrock
* Supports tool use (function calling)
* High reasoning compared to Titan models
* Enterprise privacy and compliance

Nova is Amazon’s **flagship model family** going forward.

---

# 2️⃣ **Getting Started with Nova in the Amazon Bedrock Console**

Using Nova inside AWS is extremely easy.
You don’t need to set up GPUs or containers — AWS manages everything.

Here’s how you start:

---

## ⭐ Step 1: Open Amazon Bedrock Console

Go to:
**AWS Management Console → Amazon Bedrock**

This is your main UI for interacting with foundation models.

---

## ⭐ Step 2: Enable Model Access

Bedrock requires you to enable access to each model family.

Go to:

```
Model Access → Amazon Nova → Enable
```

You can select:

* ❑ Nova Pro
* ❑ Nova Lite
* ❑ Nova Micro

---

## ⭐ Step 3: Use the Playground

The Bedrock Playground lets you test Nova interactively.

There are 3 playground options:

* **Text Playground**
* **Image Playground**
* **Multimodal Playground**

You can:

* Give text inputs
* Upload images
* Experiment with generation
* Try function calling
* Try RAG with Knowledge Bases

---

## ⭐ Step 4: Use Nova in code (Python Example)

```python
import boto3

client = boto3.client("bedrock-runtime")

response = client.converse(
    modelId="amazon.nova-pro-v1",
    messages=[{"role":"user","content":"Explain quantum computing in simple words"}]
)

print(response["output"]["message"])
```

Just change `modelId` to try different Nova variants.

---

# 3️⃣ **Multimodal Support of Amazon Nova**

Nova supports **three modalities**:

---

## ⭐ 1. **Text Input + Text Output**

* Chat
* Summaries
* Answers
* Code generation
* Reasoning
* Agents

This is the core LLM functionality.

---

## ⭐ 2. **Image Input**

Nova can understand images:

* Describe images
* Extract text
* Analyze diagrams
* Identify objects
* Reason about pictures

Example use cases:

* Document analysis
* Medical image analysis
* Product catalog automation
* Image-based chatbots

---

## ⭐ 3. **Video Input**

This is where Nova stands out — it supports video understanding.

Nova can:

* Describe video content
* Detect events in video
* Summarize video scenes
* Extract keyframes
* Explain step-by-step actions

Example use cases:

* CCTV video analysis
* Sports highlight generation
* Instructional video understanding
* Video captioning

This makes Nova a **true multimodal model**.

---

# 4️⃣ **Tool Use (Function Calling) Using Amazon Nova**

Tool Use = The ability of Nova to call your functions or APIs to perform tasks.

This is similar to:

* GPT-4 function calling
* Claude 3.5 tool use
* LangChain tool integrations

Nova can:

* Read structured tool definitions
* Decide when a tool is needed
* Call the tool with correct arguments
* Use the tool output
* Generate final answer

---

## ⭐ Why Tool Use is Important

Models can now:

* Fetch real-time data
* Query databases
* Execute business logic
* Trigger AWS Lambdas
* Run workflows
* Call internal APIs

It turns the LLM into an **AI agent**, not just a chatbot.

---

## ⭐ Tool Use Flow (Very Simple Diagram)

```
User Query → Nova Model → Decides Tool Needed →
Tool Definition → Function Call →
Tool Output → Final AI answer
```

---

## ⭐ Example of Defining a Tool (Simple JSON)

```json
{
  "name": "getWeather",
  "description": "Fetch current weather info",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {"type": "string"}
    },
    "required": ["city"]
  }
}
```

---

## ⭐ Example Chat Flow (Simplified)

User:
“What's the weather in Delhi right now?”

Nova (internal):

* Detects weather data is needed
* Calls `getWeather(city="Delhi")`

Tool returns:
`{"temperature": 27, "condition": "Clear"}`

Nova:
“Delhi is currently clear with a temperature of 27°C.”

---

# 🎉 **Final Summary — Amazon Nova Models**

### ✔ Amazon Nova is Amazon's next-generation FM family

### ✔ Available in Bedrock through API and console

### ✔ Supports text, images, and videos

### ✔ Offers fast and powerful variants (Pro, Lite, Micro)

### ✔ Strong reasoning + multimodal understanding

### ✔ Supports native tool use (function calling)

### ✔ Ideal for enterprise-grade AI applications

Nova is Amazon’s answer to OpenAI GPT-4 and Google Gemini — but built natively for AWS ecosystem.

---

