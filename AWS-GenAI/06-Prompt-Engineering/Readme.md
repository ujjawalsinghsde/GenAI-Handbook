# Prompt Engineering

Prompt engineering is the practice of designing instructions and templates that produce reliable, safe, and cost-effective outputs from large language models. Effective prompts improve accuracy, reduce hallucinations, and lower operational costs.

---

## What is Prompt Engineering?

Prompt engineering is the practice of designing clear instructions that guide AI models to produce high-quality outputs.

It involves:

- Giving explicit and structured instructions  
- Guiding the model step-by-step  
- Defining output format and tone  
- Reducing ambiguity  
- Improving consistency and accuracy  

In Bedrock (Nova, Claude, Llama), prompt clarity determines output quality.

---

## Prompt Engineering Concepts

### System Prompt  
Defines the model’s role and behavior.

Example:  
“You are a helpful AWS cloud expert who explains in simple words.”

### User Prompt  
The actual request or question.

Example:  
“Explain Amazon S3 in one paragraph.”

### Context  
Additional background information such as business rules, definitions, or prior conversation.

### Constraints  
Rules that the model must follow.

Examples:  
- “Answer in bullet points.”  
- “Limit response to 100 words.”  
- “Return output in JSON format.”

### Examples (Few-Shot Prompting)  
Provide sample inputs and outputs to define the pattern.

### Output Format  
Define expected structure — JSON, tables, lists, markdown, etc.

---

## Prompt Templates and Examples

Prompt templates allow you to reuse consistent structures.

### General Template

```
System: You are an expert assistant. Be concise and accurate.  
User: {question}  
Constraints: {rules}  
Format: {output_format}
```

### Summarization Template

```
System: You are a summarization engine.  
User: Summarize the text below in simple words.  
Text:  
{document}  
Constraints:  
- Maximum 100 words  
- Use bullet points
```

### Nova Template (JSON)

```json
{
  "system": "You are a helpful AI expert.",
  "prompt": "{user_question}",
  "format": "json"
}
```

---

## Prompting Techniques

### Zero-Shot Prompting  
Ask directly without examples. Good for simple tasks.

Example:  
“Explain serverless computing.”

### Few-Shot Prompting  
Provide examples to guide style and format.

### Output Templates  
Specify strict output structures (e.g., JSON object).

### Chain-of-Thought Prompting  
Ask the model to reason step-by-step.

### Instruction + Context Prompting  
Provide task instructions and supporting information.

### Constraint-Based Prompting  
Set explicit rules, such as word limits or structure constraints.

### Role Prompting  
Assign a role to establish tone and expertise.  
Example: “You are a senior AWS Solutions Architect.”

---

## Giving Cues and Hints to the LLM

Helpful cues include:

- “Think like a mentor.”  
- “Explain as if teaching a beginner.”  
- “Be professional.”  
- “Use simple language.”  
- “Use short paragraphs.”  

These improve clarity and control.

---

## Parsing Instructions from Content

Models can extract structured information from messy or unformatted text.

Example:

Input email:  
“Please fix the bug, deploy the new build, and send the report.”

Expected output:

- Fix the bug  
- Deploy the new build  
- Send the report  

---

## Constructing and Storing Reusable Prompt Patterns

Create a prompt library for tasks such as summarization, extraction, classification, RAG queries, and agent instructions.

Store them using one of the following:

- Git version control  
- S3  
- AWS Systems Manager Parameter Store  
- Config files  
- LangChain prompt templates  

This ensures consistency across applications.

---

## Production Considerations for Prompts

- **Version prompts with code**  
- **Run regression tests** for prompt changes  
- **Use A/B testing** for evaluation  
- **Validate user inputs** to avoid prompt injection  
- **Log prompts/responses** (mask sensitive information)  
- **Optimize token usage**  
- **Cache frequent prompts or responses**

---

## Bedrock Prompts — Detailed Study

### Model-Specific Prompting

| Model | Best For |
|-------|----------|
| Nova Pro | Deep reasoning, multimodal tasks, step-by-step explanations |
| Claude | Writing, summarization, analysis |
| Llama / Mistral | Fast, low-cost text generation |
| Titan | Embeddings and simple text |

### Bedrock Converse API Example

```python
client.converse(
  modelId="amazon.nova-pro-v1",
  messages=[
    {"role":"system","content":"You are a helpful teacher."},
    {"role":"user","content":"Explain cloud computing simply."}
  ]
)
```

### Multimodal Prompting

Nova supports text, images, and video inputs.

### Structured Outputs

```
Provide results in JSON:
{
  "title": "",
  "summary": "",
  "keywords": []
}
```

### RAG Prompting (Knowledge Bases)

“Based on the retrieved documents, answer using accurate citations.”

### Safety-Conscious Prompting

Avoid ambiguous or unsafe phrasing.

---

## Prompt Testing in Bedrock Console

You can:

- Experiment in the playground  
- Adjust parameters (temperature, max tokens)  
- Compare model behaviors  
- Test multimodal inputs  

---

## Final Summary — Prompt Engineering with Amazon Nova and Bedrock

Prompt engineering helps you:

- Control model behavior  
- Improve accuracy  
- Reduce hallucinations  
- Reduce cost  
- Produce structured, consistent outputs  

Core skills:

- Creating reusable templates  
- Using zero-shot and few-shot prompting  
- Setting clear instructions and constraints  
- Using role-based prompts  
- Defining output formats (especially JSON)  
- Working with multimodal inputs  
- Guiding reasoning  
- Combining prompts with RAG and tools  

Bedrock + Nova provides a robust stack for building production-grade GenAI applications.

