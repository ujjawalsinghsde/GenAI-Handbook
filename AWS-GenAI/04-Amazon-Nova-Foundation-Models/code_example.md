# Python Code Examples for Amazon Nova (Bedrock)

Before running any example, ensure you have:

```bash
pip install boto3
```

And your AWS credentials configured:

```
aws configure
```

---

# Basic Text Generation using Amazon Nova Pro

```python
import boto3

client = boto3.client("bedrock-runtime")

response = client.converse(
    modelId="amazon.nova-pro-v1",
    messages=[
        {"role": "user", "content": "Explain what quantum computing is in simple words."}
    ]
)

print(response["output"]["message"]["content"])
```

This example prints the model response returned by Nova Pro.

---

# Using Amazon Nova Lite

```python
import boto3

client = boto3.client("bedrock-runtime")

response = client.converse(
    modelId="amazon.nova-lite-v1",
    messages=[
        {"role": "user", "content": "Write a short welcome message for my app."}
    ]
)

print(response["output"]["message"]["content"])
```

`nova-lite` provides lower latency and cost for high-volume use cases.

---

# Using Amazon Nova Micro (Ultra-fast model)

```python
import boto3

client = boto3.client("bedrock-runtime")

response = client.converse(
    modelId="amazon.nova-micro-v1",
    messages=[
        {"role": "user", "content": "Give a short motivational quote."}
    ]
)

print(response["output"]["message"]["content"])
```

`nova-micro` is suitable for ultra-low-latency or on-device scenarios.

---

# Image Understanding With Amazon Nova (Multimodal Example)

```python
import boto3
import base64

client = boto3.client("bedrock-runtime")

# Load image
with open("image.jpg", "rb") as f:
    image_bytes = base64.b64encode(f.read()).decode("utf-8")

response = client.converse(
    modelId="amazon.nova-pro-v1",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Describe this image in detail."},
                {
                    "type": "input_image",
                    "image": {
                        "format": "jpeg",
                        "source": {"bytes": image_bytes}
                    }
                }
            ]
        }
    ]
)

print(response["output"]["message"]["content"])
```

Nova can extract structured descriptions from images when supplied with proper image data.

---

# Video Understanding With Amazon Nova (Multimodal)

```python
import boto3
import base64

client = boto3.client("bedrock-runtime")

# Load a video clip
with open("clip.mp4", "rb") as f:
    video_bytes = base64.b64encode(f.read()).decode("utf-8")

response = client.converse(
    modelId="amazon.nova-pro-v1",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Summarize what happens in this video."},
                {
                    "type": "input_video",
                    "video": {
                        "format": "mp4",
                        "source": {"bytes": video_bytes}
                    }
                }
            ]
        }
    ]
)

print(response["output"]["message"]["content"])
```

Nova can analyze scenes, actions, transitions, and events in video inputs when provided.

---

# Tool Use (Function Calling) With Amazon Nova

This is a powerful capability: Nova can decide when to call a registered function.

### Step 1 — Define Tool Schema

```python
tools = [
    {
        "toolSpec": {
            "name": "getWeather",
            "description": "Get current weather of a city.",
            "inputSchema": {
                "json": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"}
                    },
                    "required": ["city"]
                }
            }
        }
    }
]
```

---

### Step 2 — Create a Function That Nova Can Call

```python
def getWeather(city):
    # Dummy example — replace with real API call
    return {"temperature": 27, "condition": "Clear"}
```

---

### Step 3 — Call Nova With Tools Enabled

```python
import boto3
import json

client = boto3.client("bedrock-runtime")

user_query = "What's the weather in Delhi right now?"

response = client.converse(
    modelId="amazon.nova-pro-v1",
    messages=[{"role": "user", "content": user_query}],
    tools=tools
)

tool_call = response["output"]["message"].get("toolUse")
```

---

### Step 4 — Execute Tool if Nova Calls It

```python
if tool_call:
    tool_name = tool_call["name"]
    args = tool_call["input"]

    if tool_name == "getWeather":
        tool_output = getWeather(**args)

    final_response = client.converse(
        modelId="amazon.nova-pro-v1",
        messages=[
            {"role": "assistant", "content": response["output"]["message"]["content"]},
            {
                "role": "tool",
                "name": tool_name,
                "content": json.dumps(tool_output)
            }
        ]
    )

    print(final_response["output"]["message"]["content"])
else:
    print(response["output"]["message"]["content"])
```

Nova may decide when a tool is required, call it, and use the tool output to produce the final answer.

---

# RAG (Retrieval-Augmented Generation) With Nova — Mini Example

```python
import boto3

client = boto3.client("bedrock-runtime")

response = client.retrieve_and_generate(
    input={"text": "What does the refund policy say about digital items?"},
    knowledgeBaseId="your-kb-id"
)

print(response["output"]["text"])
```

This example uses Bedrock Knowledge Base with Nova to answer based on internal documents.

---

# Final Summary of Code Examples Provided

| Feature                  | Example provided        |
| ------------------------ | ----------------------- |
| Text generation          | Nova Pro, Lite, Micro   |
| Image understanding      | Image input example     |
| Video understanding      | Video input example     |
| Function calling         | Tool use example        |
| RAG using Knowledge Base | Simple KB call          |
| Bedrock Converse API     | Used in examples        |

---
