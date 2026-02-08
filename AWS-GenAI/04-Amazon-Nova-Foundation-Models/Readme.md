# Amazon Nova — Foundational Models

Amazon Nova is a family of foundation models available via Amazon Bedrock. Nova variants provide multimodal inputs, enhanced reasoning, and function-calling capabilities suitable for enterprise workflows.

## Amazon Nova — Family of Foundation Models

Amazon Nova is Amazon’s family of foundation models, designed for multimodal inputs, advanced reasoning, and function-calling suitable for enterprise workflows. Nova models are available in three primary variants.

---

### Amazon Nova Pro

- Most powerful Nova model
- High reasoning capability
- Best for: agents, knowledge assistants, advanced chatbots, and complex enterprise use cases

Consider Nova Pro for tasks that require the highest reasoning accuracy and tool integration.

---

### Amazon Nova Lite

- Smaller and more cost-effective
- Good for fast responses, lightweight reasoning, low-latency chatbots, and high-volume applications

Choose Nova Lite when latency and cost are primary concerns.

---

### Amazon Nova Micro

- Tiny and ultra-fast
- Useful for autocomplete, simple classification, on-device inference, and quick suggestions

Use Nova Micro for extremely low-latency or resource-constrained scenarios.

---

## Common Features Across Nova Models

- Multimodal (text, images, video)
- Lower hallucination rates compared to general-purpose models
- Efficient and scalable for production use
- Native Bedrock integration and tooling
- Support for structured function calling (tool use)
- Enterprise privacy and compliance features

Nova is positioned as Amazon’s flagship model family for Bedrock.

---

## Getting Started with Nova in the Amazon Bedrock Console

Nova is accessible via the Bedrock Console; AWS manages infrastructure so you do not need GPUs or containers.

### Step 1 — Open the Bedrock Console

Navigate to: AWS Management Console → Amazon Bedrock. This is the primary UI for interacting with Nova models.

### Step 2 — Enable Model Access

Enable access to Nova in the Model Access settings (Model Access → Amazon Nova → Enable).

Available variants:

- Nova Pro
- Nova Lite
- Nova Micro

### Step 3 — Use the Playground

Try the Bedrock Playground (Text, Image, or Multimodal) to experiment with generation, function calling, and RAG integrations.

### Step 4 — Use Nova in code (Python example)

```python
import boto3

client = boto3.client("bedrock-runtime")

response = client.converse(
  modelId="amazon.nova-pro-v1",
  messages=[{"role":"user","content":"Explain quantum computing in simple words"}]
)

print(response["output"]["message"])
```

Change `modelId` to switch variants.

---


## Multimodal Capabilities

Nova accepts text, image, and video inputs. Use multimodal inputs for cross-modal tasks (document images, diagrams, instructional video). Ensure preprocessing (OCR, frame sampling) and multimodal retrieval are validated.

## Function Calling and Tool Use

Nova supports structured function calling. Define explicit tool schemas, validate tool outputs, and enforce allowlists and input validation to reduce risk.

### Why tool use matters

Tools allow models to fetch real-time data, query databases, execute business logic, trigger Lambdas, run workflows, and call internal APIs — converting LLMs into action-capable agents.

### Tool use flow (simple)

```
User Query → Nova Model → Decides Tool Needed → Tool Definition → Function Call → Tool Output → Final AI answer
```

---

## Example of Defining a Tool (JSON)

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

## Example Chat Flow (Simplified)

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



## Summary and Production Notes

- Nova provides production-grade multimodal models via Bedrock.
- Choose the appropriate variant: `pro` for high-reasoning tasks, `lite` for latency-sensitive workloads, and `micro` for low-cost or on-device use cases.
- For function-calling: restrict tool permissions, validate inputs/outputs, and audit tool invocations.
- For multimodal tasks: ensure preprocessing pipelines (OCR, frame extraction) are robust and reproducible.
- Monitor cost, latency, and hallucination rates; use RAG to ground factual answers when appropriate.

Supports native tool use (function calling) and is suitable for enterprise-grade AI applications in the AWS ecosystem.

---

