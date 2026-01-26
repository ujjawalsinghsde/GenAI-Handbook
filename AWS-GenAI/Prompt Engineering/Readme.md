# 📘 **Prompt Engineering**

Prompt engineering is one of the most important skillsets when working with large language models (LLMs) like Amazon Nova, Claude, or Llama on Amazon Bedrock.
Good prompts = better answers, lower cost, lower hallucination, and higher accuracy.

---

# 1️⃣ **What is Prompt Engineering?**

**Prompt Engineering is the art of designing and writing instructions that help AI models produce the best possible output.**

Think of it like:

* Giving clear instructions to an assistant
* Guiding the AI step-by-step
* Making the model follow structure, tone, and rules
* Reducing confusion and improving accuracy

When you use Bedrock models (Nova, Claude, Llama), **your prompt decides EVERYTHING**.

---

# 2️⃣ **Prompt Engineering Concepts**

These are the fundamental building blocks.

---

## ⭐ 2.1 System Prompt

Tells the model *who it should act as*.

Example:

> “You are a helpful AWS cloud expert who explains in simple words.”

This sets the AI’s personality and behavior.

---

## ⭐ 2.2 User Prompt

The actual question or request.

Example:

> “Explain Amazon S3 in one paragraph.”

---

## ⭐ 2.3 Context

Additional data you give the model.

Example:

* Background information
* Definitions
* Business rules
* Conversation history

---

## ⭐ 2.4 Constraints

Rules the model must follow.

Examples:

* “Answer in bullet points.”
* “Limit to 100 words.”
* “Return output in JSON format.”

---

## ⭐ 2.5 Examples (Few-shot prompting)

Provide sample inputs/outputs to guide behavior.

---

## ⭐ 2.6 Output Format

Tell the model how to respond:

* JSON
* Table
* Numbered list
* Markdown

---

# 3️⃣ **Prompt Templates & Examples**

Prompt templates help you reuse consistent patterns.

---

## ⭐ Example Template (General)

```
System: You are an expert assistant. Be concise and accurate.
User: {question}
Constraints: {rules}
Format: {output_format}
```

---

## ⭐ Example: Summarization Template

```
System: You are a summarization engine.
User: Summarize the text below in simple words.
Text:
{document}
Constraints:
- Max 100 words
- Use bullet points
```

---

## ⭐ Example: Nova in Bedrock Template

```json
{
  "system": "You are a helpful AI expert.",
  "prompt": "{user_question}",
  "format": "json"
}
```

---

# 4️⃣ **Prompting Techniques**

Let’s understand the most important prompting methods in simple words.

---

## ⭐ 4.1 Zero-Shot Prompting

*No examples provided.*
Just ask the question directly.

Example:

> “Explain serverless computing.”

Good for simple tasks.

---

## ⭐ 4.2 Few-Shot Prompting

*Provide examples so the model learns the pattern.*

Example:

```
Example:
Q: What is S3?
A: S3 is AWS storage service.

Now answer:
Q: What is EC2?
```

Few-shot prompting = better consistency.

---

## ⭐ 4.3 Output Templates

Tell the model the exact structure to follow.

Example (JSON):

```
Return the results in JSON:
{
  "definition": "",
  "use_cases": [],
  "example": ""
}
```

Nova follows structure more accurately this way.

---

## ⭐ 4.4 Chain-of-Thought (Reasoning Prompting)

Tell the model to think step-by-step.

Example:

> “Think step-by-step and explain how Amazon VPC works.”

Nova Pro follows reasoning extremely well.

---

## ⭐ 4.5 Instruction + Context Prompting

Provide instructions + data in the same prompt.

Example:

```
Instruction:
Summarize the document.
Context:
{text}
```

---

## ⭐ 4.6 Constraint-Based Prompting

Add strict rules.

Example:

> “Explain Lambda in exactly 4 sentences.”

---

## ⭐ 4.7 Role Prompting

Define a role:

> “You are a senior AWS Solutions Architect.”

Gives more reliable and professional outputs.

---

# 5️⃣ **Providing Cues & Hints to the LLM**

Cues help the model understand your expectations.

Examples:

* “Think like a mentor.”
* “Explain as if teaching a beginner.”
* “Answer professionally.”
* “Use simple words.”
* “Use short paragraphs.”
* “Focus only on AWS.”

These cues reduce confusion and improve clarity.

---

# 6️⃣ **Parsing Instructions from Content**

Models can extract instructions from complex or messy inputs.

Example:

```
Here is a messy email. Extract only the action items:

Email:
"Hey team, please fix the bug, deploy the new build, and send report."
```

Output:

* Fix bug
* Deploy new build
* Send report

You can create parsing prompts:

```
Parse the following content into a clean task list:
{text}
```

---

# 7️⃣ **Construct & Store Reusable Prompt Patterns**

In real applications, you will create reusable patterns for:

* Summarization
* Classification
* Extraction
* Agent instructions
* RAG queries
* Customer support
* Data cleaning
* JSON generation

Store them in:

* DynamoDB
* S3
* Config files
* LangChain prompt templates
* Bedrock agents

This ensures consistent behavior across your entire application.

---

# 8️⃣ **Bedrock Prompts — Detailed Study**

Prompts in Bedrock follow certain rules and best practices.

---

## ⭐ 8.1 Model-Specific Prompting

Each model behaves differently:

| Model             | Best For                                 |
| ----------------- | ---------------------------------------- |
| **Nova Pro**      | Deep reasoning, multimodal, step-by-step |
| **Claude**        | Writing, summarization, analysis         |
| **Llama/Mistral** | Fast, low-cost APIs                      |
| **Titan**         | Embeddings, simple text                  |

So prompts must be adapted per model.

---

## ⭐ 8.2 Bedrock Converse API Prompting (Text)

Example:

```python
client.converse(
  modelId="amazon.nova-pro-v1",
  messages=[
    {"role":"system","content":"You are a helpful teacher."},
    {"role":"user","content":"Explain cloud computing simply."}
  ]
)
```

---

## ⭐ 8.3 Multimodal Prompting (Nova)

You can mix:

* text
* image
* video

Example:

```json
{
  "messages":[
    {
      "role":"user",
      "content":[
        {"type":"input_text", "text":"Describe this image:"},
        {"type":"input_image","image":{...}}
      ]
    }
  ]
}
```

---

## ⭐ 8.4 Structured Outputs

Bedrock models obey structure better when told clearly:

```
Provide answer in JSON:
{
  "title": "",
  "summary": "",
  "keywords": []
}
```

---

## ⭐ 8.5 RAG Prompting (Knowledge Base)

Example:

```
Based on the retrieved documents, answer the question using accurate citations.
```

Bedrock automatically injects chunks into the LLM.

---

## ⭐ 8.6 Safety-Conscious Prompting

Prompts should avoid:

* Ambiguity
* Unsafe content
* Open-ended questions without context

Example:

❌ “Tell me about drugs”
✔ “Explain the harmful effects of drugs for educational purposes.”

---

## ⭐ 8.7 Prompt Testing in Bedrock Console

You can:

* Experiment in Playgrounds
* Adjust temperature
* Add instructions
* Compare models
* Test multimodal prompts

This helps refine prompts before API deployment.

---

# 🎉 **Final Summary — Prompt Engineering with Amazon Nova & Bedrock**

Prompt Engineering helps you:

* Control model behavior
* Improve accuracy
* Reduce hallucinations
* Reduce cost
* Get consistent, structured outputs
* Build production-ready GenAI apps

Key skills:

* Creating templates
* Using zero-shot & few-shot prompting
* Giving clear instructions + constraints
* Using role-based prompts
* Using output formats (especially JSON)
* Managing multimodal inputs
* Guiding reasoning using chain-of-thought
* Using Bedrock agents & tools

Nova + Bedrock is a powerful combination for building real AI systems.

---
