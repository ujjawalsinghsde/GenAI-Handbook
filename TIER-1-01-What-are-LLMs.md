# TIER 1-01: What Are LLMs?
## The Definition, in Simple Terms

---

## Simple Definition

An **Large Language Model** is a neural network that learned to predict the next word by reading billions of words from the internet.

That's it. That's an LLM.

```
Input: "The capital of France is"
LLM: *thinks about billions of examples it saw*
LLM: "Paris" is the most likely next word
```

---

## Breaking Down "Large Language Model"

### "Large"
The model has billions of parameters (weights in the network).

```
Small model: 7 billion parameters
Medium model: 70 billion parameters
Large model: 175 billion parameters (GPT-3)
Very large: 1.8 trillion parameters (estimated GPT-4)
```

More parameters = can learn more complex patterns = slower to train and run = more expensive.

### "Language"
It's trained on human language (text). It understands grammar, meaning, context, and can reason about language.

(As opposed to image models trained on pictures, or audio models trained on sounds.)

### "Model"
A trained neural network. The "learned patterns" frozen in time, ready to use.

```
Before training: Random weights (useless)
Training: Adjust weights based on data
After training: Frozen weights (the "model")

The model is the end result. You use it without changing it further.
(Unless you fine-tune, but that's a different tier.)
```

---

## What LLMs Are Actually Good At

### ✅ Generating Text
```
Prompt: "Write a poem about AI"
LLM: [generates a poem]
```

### ✅ Answering Questions
```
Prompt: "What is photosynthesis?"
LLM: [explains photosynthesis]
```

### ✅ Summarizing
```
Prompt: "Summarize this article in 3 sentences"
LLM: [provides 3-sentence summary]
```

### ✅ Translating
```
Prompt: "Translate to Spanish: Hello world"
LLM: "Hola mundo"
```

### ✅ Code Generation
```
Prompt: "Write Python code to calculate factorial"
LLM: [generates working code]
```

### ✅ Reasoning (Limited)
```
Prompt: "If all birds have wings, and Tweety is a bird, does Tweety have wings?"
LLM: "Yes" (applies logic, though it can fail on harder problems)
```

---

## What LLMs Are Bad At

### ❌ Real-Time Data
```
Prompt: "What's the stock price of Apple right now?"
LLM: "I don't know - my training data is from 2023"

(It can't browse the internet. It only knows what it learned during training.)
```

### ❌ Arithmetic (Surprising!)
```
Prompt: "What is 347 × 892?"
LLM: [often gets it wrong, might say 309,000+ instead of 309,524]

(It learned approximate patterns about numbers, not precise calculation)
```

### ❌ Reasoning About New Facts
```
Prompt: "John has 3 apples. Mary has twice as many. How many do they have together?"
LLM: [Might get it right, might not - depends on how similar examples it saw during training]

(It's not actually "calculating" like a calculator. It's predicting what usually comes after this pattern.)
```

### ❌ Making up Facts (Hallucination)
```
Prompt: "Who won the 1987 World Series?"
LLM: "The Boston Red Sox won"
Fact: "Wrong - it was the Minnesota Twins"

(The model confident-ly made up an answer that sounded plausible but was false.)
```

### ❌ Perfect Consistency
```
Turn 1: "AI is amazing" (positive opinion)
Turn 10: "AI is overrated" (negative opinion)
You: "Wait, you just said it was amazing!"
LLM: "Yes, but..."

(It doesn't maintain a consistent worldview across conversations or even within conversations.)
```

---

## How LLMs are Trained

### Phase 1: Pre-training (The Expensive Part)

```
Input: Every piece of text they could find online
- Wikipedia
- Reddit
- News articles
- Books
- Code repositories
- GitHub
- Basically, the entire internet

Total data: Hundreds of billions to trillions of tokens

Training task: Predict the next word

Training time: Months
Computing power: Thousands of GPUs working together
Cost: Millions of dollars
```

**The result:** A model that's pretty good at predicting the next word.

This pre-trained model is surprisingly intelligent, even without any further training.

```
Pre-trained model on the internet: Already knows about science, history, programming, jokes, etc.
```

### Phase 2: Instruction Fine-Tuning (Making It Useful)

Pre-trained models are weird. They're trained on *predicting the next word*, so they respond to anything:

```
Pre-trained GPT-3:
Prompt: "Hello, how are you?"
Output: "I appreciate the question. My mother used to say that happiness is..."
         [continues rambling incoherently]

It's not trying to answer your question. It's just continuing text in the style of the internet!
```

To fix this, researchers:
1. Write examples of good question-answer pairs (thousands of them)
2. Fine-tune the model to respond helpfully
3. Result: ChatGPT (helpful, harmless, honest)

```
Fine-tuned GPT-3.5 (ChatGPT):
Prompt: "Hello, how are you?"
Output: "I'm doing well, thanks for asking! How can I help you?"

Much better!
```

### Phase 3: Reinforcement Learning from Human Feedback (RLHF)

Fine-tuned models are good, but still make mistakes. To improve:

1. Generate multiple responses to the same prompt
2. Have humans rank them (best to worst)
3. Train a "reward model" to predict what humans like
4. Adjust the main model to maximize reward from human evaluators

```
Prompt: "Explain quantum computing"

Response 1 (complex, technical): "Quantum computers use superposition..."
Response 2 (clear, simple): "Quantum computers are like magical coins..."

Human evaluation:
"Response 2 is better - easier to understand for a general audience"

Reward model learns: "Simple explanations get higher rewards"
Main model adjusts to generate more like Response 2
```

---

## LLMs vs. Other AI

| Type | What It Does | Example |
|------|-----------|---------|
| **Image Recognition** | Classifies images | "This is a cat" |
| **Language Model (LLM)** | Generates or understands text | "Write me a story" |
| **Object Detection** | Finds objects in images | "Cat at (200, 150)" |
| **Speech Recognition** | Converts speech to text | "Hello" → "hello" |
| **Translation Model** | Translates between languages | English → Spanish |
| **Recommender System** | Suggests items | "You might like this movie" |

**Key difference:** LLMs are *generative* (create new text). Most others are *discriminative* (classify or recognize existing things).

---

## Types of LLMs

### 1. Chat Models (Assistant-Style)
Trained to have conversations and answer questions.

Examples: ChatGPT, Claude, Gemini

```
Prompt: "What is machine learning?"
Response: "Machine learning is a subfield of AI..."
```

### 2. Base Models (Raw Text Predictors)
Pure next-word predictors, no instruction fine-tuning.

Examples: GPT-3 (before fine-tuning), LLaMA

```
Prompt: "The future of AI"
Response: "...is vast and uncertain. Some experts believe..."
         (continues in the style of internet text)
```

### 3. Specialized Models
Trained for specific domains.

Examples:
- Medical: BioBERT (trained on medical papers)
- Code: Codex (trained on GitHub code)
- Math: Galactica (trained on mathematical papers)

```
Medical model + medical prompt = accurate medical info
General model + medical prompt = might be inaccurate
```

### 4. Open Source vs. Proprietary
**Open Source:** Code and weights publicly available. You can run it yourself.
- LLaMA (Meta)
- Mistral
- Alpaca

**Proprietary:** Closed. You access via API.
- GPT-4 (OpenAI)
- Claude (Anthropic)
- Gemini (Google)

Trade-offs:
```
Open Source:
- Pro: Free (if you have compute)
- Pro: Complete control
- Con: You have to host and maintain it
- Con: Usually slightly less capable

Proprietary:
- Pro: Cutting-edge capability
- Pro: No hosting hassle
- Con: Pay per token
- Con: Your data goes to their servers
```

---

## LLM Architecture (Quick Recap)

You already learned this in TIER 0, but here's a reminder:

```
Input text
  ↓
Tokenization (break into tokens)
  ↓
Embedding (convert to vectors)
  ↓
Transformer blocks (96 layers, each with attention)
  ↓
Predicting probability of next token
  ↓
Convert back to text

Output: Next token(s)
```

The model runs this multiple times to generate a full response:
- Generate token 1 → most likely is "The"
- Generate token 2 → given "The", most likely is "machine"
- Generate token 3 → given "The machine", most likely is "learning"
- And so on...

---

## Context and Memory

### The Problem
LLMs process one prompt at a time. They don't have a permanent memory.

```
Conversation:
You: "My name is John"
LLM: "Nice to meet you, John!"

Later...

You: "What's my name?"
LLM: "I don't know - I don't have access to previous conversations"
```

### The Solution
In chat interfaces, the entire conversation history is sent as context:

```
Turn 1:
You: "My name is John"
LLM sees: "My name is John"
LLM: "Nice to meet you, John!"

Turn 2:
You: "What's my name?"
LLM sees: [entire conversation history]
         "My name is John... [previous response]... What's my name?"
LLM: "Your name is John"
```

**Important:** The entire conversation history counts toward token usage!

```
Turn 1: 10 input + 50 output = 60 tokens
Turn 2: 10 input + 60 output = 70 tokens
       (But the LLM actually sees: 10 + 50 + 10 + 60 = 130 tokens internally!)

Most APIs only charge you for new tokens (10 + 60), not the full conversation
```

### Context Window Limit
There's a maximum length the model can handle:

```
GPT-3.5: 4,096 tokens
Claude 3: 200,000 tokens

If your conversation + new prompt exceeds this, you get an error or loss of early context.
```

---

## Real-World Examples

### Example 1: Customer Support Bot
```
Pre-trained model: Knows patterns of language
Fine-tuned on: Customer support conversations
Used for: Answering FAQ about returns, shipping, etc.

LLM can:
✅ Understand customer questions
✅ Generate helpful responses
❌ Access the actual shipping database (needs integration)
```

### Example 2: Content Writing Assistant
```
Pre-trained model: Knows English grammar and style
Fine-tuned on: Good writing examples
Used for: Helping write blog posts

LLM can:
✅ Write in different styles
✅ Generate multiple versions
❌ Verify facts (might make up sources)
```

### Example 3: Programming Assistant (Copilot)
```
Pre-trained model: Trained on billions of GitHub repositories
Fine-tuned on: Good code examples
Used for: Suggesting code as you type

LLM can:
✅ Suggest working code patterns
✅ Complete functions
❌ Guarantee bug-free code (might have subtle bugs)
```

---

## Self-Check

Can you answer:

- [ ] "What is an LLM in simple terms?" (A neural network trained to predict the next word)
- [ ] "What are LLMs good at?" (Generating text, answering questions, code, reasoning)
- [ ] "What are they bad at?" (Real-time data, precise arithmetic, hallucinations, consistency)
- [ ] "What's the difference between pre-training and fine-tuning?" (Pre-training learns patterns from data; fine-tuning teaches it to follow instructions)
- [ ] "Do LLMs have memory across conversations?" (No - each conversation is separate unless you include full history)
- [ ] "What's a context window?" (Maximum tokens the model can process)

If you got these, you're ready for **[TIER-1-02-How-LLMs-Generate-Text.md](TIER-1-02-How-LLMs-Generate-Text.md)** →

This document explains the actual process step-by-step.
