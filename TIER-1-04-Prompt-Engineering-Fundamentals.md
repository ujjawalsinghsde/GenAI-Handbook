# TIER 1-04: Prompt Engineering Fundamentals
## How to Write Prompts That Work

---

## What is Prompt Engineering?

**Prompt Engineering:** Writing instructions that get LLMs to do what you want.

The better your prompt, the better the response. It's a real skill you need to master.

```
Bad prompt: "Tell me about AI"
Response: [Generic overview, probably unhelpful]

Good prompt: "Explain how transformer neural networks work, 
as if you're teaching a software engineer with no ML background.
Use code-like pseudocode if helpful. Keep under 300 words."
Response: [Clear, technical, well-scoped]
```

---

## The Core Principles

### 1. Be Specific

Vague prompts get vague responses.

```
❌ Vague: "Explain machine learning"

✅ Specific: "Explain machine learning to someone with 5 years of 
programming experience but no ML background. Focus on the 
practical differences between supervised and unsupervised learning 
with real examples."
```

**Why it matters:** LLMs respond to your exactness. Specify:
- Who is the audience?
- What's the purpose?
- What constraints exist?

### 2. Provide Context

LLMs work better when they understand the bigger picture.

```
❌ Without context: "What should I do next?"

✅ With context: "I'm building a chatbot for customer support.
I've implemented basic Q&A, but customers often ask about 
return policies. What should I add next?"
```

Context helps the model give relevant advice.

### 3. Give Examples (Few-Shot Learning)

Show examples of what you want.

```
❌ No examples: "Classify this email as spam or not spam:
'You've won a prize! Click here to claim it.'"

✅ With examples: "Classify emails as SPAM or NOT_SPAM.

Example 1:
Email: 'Meeting tomorrow at 3pm?'
Classification: NOT_SPAM

Example 2:
Email: 'You've won $1000! Click now!'
Classification: SPAM

Example 3:
Email: 'Password reset confirmation sent'
Classification: NOT_SPAM

Now classify this: 'You've won a prize! Click here to claim it.'"
```

Examples show the pattern you want the model to follow.

### 4. Break Complex Tasks Into Steps

For complicated requests, ask for step-by-step thinking.

```
❌ Direct: "Write me a business plan"

✅ Structured: "Write a business plan with these sections:
1. Executive Summary (2 paragraphs)
2. Market Analysis (how big is the market? who are competitors?)
3. Revenue Model (how will you make money?)
4. 3-Year Financial Projections
5. Key Risks and Mitigations

Use realistic numbers. Target market: small business accounting software."
```

Breaking it down helps the model stay focused.

### 5. Specify the Format

Tell the model what format you want.

```
❌ Unspecified: "Tell me about the top 5 AI companies"

✅ Specified: "List the top 5 AI companies by market cap.
Format as a table with columns: Company | Market Cap | Founded | Headquarters.
Include only companies primarily in AI (not tech companies with AI divisions)."
```

Format specifications prevent rambling and ensure usability.

---

## Prompt Techniques

### Technique 1: System Prompt

Set the model's role and behavior:

```
System: "You are an expert software architect with 20 years of experience.
You explain complex topics clearly but precisely.
You challenge assumptions respectfully.
You use real-world examples."

User: "How should I design a database for 10 million users?"

Result: Response is from the perspective of an expert architect, 
more thoughtful and detailed than a generic answer.
```

### Technique 2: Chain-of-Thought (CoT)

Ask the model to show its reasoning:

```
❌ Regular: "If John has 3 apples and Mary has twice as many, 
how many do they have together?"

✅ Chain-of-Thought: "If John has 3 apples and Mary has twice as many, 
how many do they have together? 
Think through this step by step and show your work."

Result: Model shows reasoning, making errors easier to spot and correct.
```

### Technique 3: Temperature Hints

Subtly influence randomness through wording:

```
For creative output:
"Generate 5 unique and unexpected approaches to..."

For factual output:
"Provide the most accurate and precise answer to..."
```

### Technique 4: Role-Playing

```
❌ Regular: "Explain why Vue.js is useful"

✅ Role-play: "You are a React expert who just learned Vue.js.
Explain to your team why Vue.js is useful for our next project.
Be honest about tradeoffs."

Result: More nuanced, considers multiple perspectives.
```

### Technique 5: Iterative Refinement

```
You: "Explain RAG"
LLM: [Gets explanation]

You: "That's too technical. Simplify it for a 14-year-old"
LLM: [Better, simpler explanation]

You: "Add an analogy about how you remember things"
LLM: [Refined with analogy]
```

Each iteration refines the response.

---

## Real-World Prompt Examples

### Example 1: Code Generation

```
Good Prompt:
"Write Python code that:
1. Reads a CSV file with columns: name, email, signup_date
2. Filters for users who signed up in the last 30 days
3. Sends them a welcome email
4. Logs results to a file

Use:
- async/await for email sending
- Error handling for network failures
- Comments explaining each section
- No external dependencies except 'aiosmtplib' and 'pandas'"

Result: Specific, working code that matches requirements.
```

### Example 2: Content Writing

```
Good Prompt:
"Write a LinkedIn post (150-200 words) about 'The Future of AI in Business'.

Tone: Professional, optimistic but realistic
Include: 1 statistic, 1 question for engagement
Format: Paragraph format with line breaks for readability
Avoid: AI jargon (assume audience is non-technical business people)
Goal: Get engagement, so end with a question"

Result: Posts optimized for the platform and audience.
```

### Example 3: Debugging Help

```
Good Prompt:
"I'm getting an error when calling this API endpoint.

Error: 'ConnectionError: max retries exceeded'
Environment: Python 3.11, requests library 2.28

Code snippet:
[code here]

I've already tried:
- Checking if server is up (it is, tested with curl)
- Increasing timeout to 30 seconds
- Verifying credentials

What else should I try?
Next steps for debugging this issue?"

Result: Useful debugging suggestions based on context.
```

### Example 4: Interview Prep

```
Good Prompt:
"Prepare me for a software engineer interview at Google.

My background:
- 3 years experience, mostly frontend (React/TypeScript)
- Some backend experience (Node.js)
- Never done serious algorithm problems

The interview:
- 60 minutes
- Coding problem + discussion

For each topic, give me:
1. Key concepts to know
2. 2-3 practice problems
3. Common mistakes
4. How to explain my solution clearly"

Result: Targeted, useful interview prep.
```

---

## Common Mistakes

### ❌ Mistake 1: Asking Too Many Questions at Once

```
Bad: "What is AI? How does machine learning work? What are neural 
networks? Why are transformers important? How do you train an LLM?"

Good: Ask one question, then follow up with related questions based on answers.
```

### ❌ Mistake 2: Assuming the Model Knows Your Context

```
Bad: "How should I structure my project?"
(Model doesn't know what your project is)

Good: "I'm building a real-time chat application. I expect 10,000 
concurrent users. The stack is Next.js frontend and Python backend. 
How should I structure the project?"
```

### ❌ Mistake 3: Forgetting to Specify Constraints

```
Bad: "Write a summary"

Good: "Write a 2-3 sentence summary for a busy executive. 
Focus on business impact, not technical details."
```

### ❌ Mistake 4: Not Iterating

```
Bad: Accept the first response and use it
Good: Ask follow-ups to refine:
- "Can you add more examples?"
- "That's too technical, simplify it"
- "Focus only on the business aspect"
```

---

## Advanced Techniques

### Technique: Temperature in Prompting

```
For deterministic tasks:
"Provide THE correct answer to..." (implies low temperature)

For creative tasks:
"Brainstorm 10 wildly creative and unexpected ways..." (implies high temperature)
```

### Technique: Persona Stacking

```
"You are a product manager + software architect + business analyst.
From all three perspectives, explain why we should build feature X."

Different perspectives often catch things one viewpoint misses.
```

### Technique: Reverse Prompting

```
Instead of: "Explain why RAG is useful"
Try: "Explain why RAG might NOT be useful. What are the downsides?"

Getting counterarguments often reveals what you're missing.
```

---

## Tools for Prompt Development

### Manual Testing
1. Write prompt
2. Run it 3-5 times
3. Observe consistency and quality
4. Refine based on results

### Iterative Refinement
```
Start → Test → Observe → Adjust → Test → Repeat until satisfied
```

### Prompt Versioning
```
v1: Original prompt
v2: Add more context
v3: Add examples
v4: Change tone

Track what works and why.
```

---

## Self-Check

Can you improve these prompts?

```
❌ "Explain React"
✅ Better version: ?

❌ "Write code that does X"
✅ Better version: ?

❌ "Is this good?"
✅ Better version: ?

(Answers in next section)
```

**Suggested answers:**

```
✅ "Explain React to someone who knows JavaScript but not frontend frameworks.
Focus on: components, hooks, state management. 
Keep it under 500 words. Use a simple example."

✅ "Write Python code that:
1. [requirement 1]
2. [requirement 2]
Include error handling and comments.
Use these libraries: [specific versions]"

✅ "Evaluate this code for:
1. Security: any vulnerabilities?
2. Performance: any optimizations?
3. Readability: is it clear?
Rate each 1-10 and explain why."
```

Ready for **[TIER-1-05-Limitations-and-Hallucinations.md](TIER-1-05-Limitations-and-Hallucinations.md)** →

Next: Understanding what LLMs can't do, and how to work with that.
