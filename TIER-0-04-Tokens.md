# TIER 0-04: Tokens
## Why Language Models Charge Per Token (And How It Works)

---

## What is a Token?

A token is **a piece of text**. But not always a word.

Sometimes it's a whole word. Sometimes it's a syllable. Sometimes it's a single character.

```
Examples:
"hello" → 1 token
"world" → 1 token
"incredible" → 2 tokens
"!" → 1 token
" " (space) → 1 token (sometimes)
"Æ" → 1 token (sometimes combined with neighbors)
```

**Key rule:** Languages with more syllables per word have more tokens per word.

```
English: "Hello, how are you?" → ~6-7 tokens
Spanish: "Hola, ¿cómo estás?" → ~7-8 tokens (slightly more due to special characters)
Japanese: Same meaning → ~15-20 tokens (because Japanese works differently)
```

---

## Why Tokens Instead of Words?

The model needs to process text, but there are millions of possible words (including made-up ones, typos, rare words).

**Solution:** Break everything into smaller pieces called tokens.

```
Vocabulary: 50,000 tokens

These 50,000 tokens can represent:
- Common words: "the", "hello", "incredible"
- Rare words: "serendipitous" = multiple tokens
- Words it's never seen: Break into known pieces

"pneumonoultramicroscopicsilicovolcanoconiosis"
(longest word in English) → 12 tokens

But even a 50,000-token vocabulary can cover almost all text!
```

---

## Tokenization Process

### Step 1: Encoding
Converting text to tokens (numbers):

```
Text: "Hello, how are you?"

Tokens: [9906, 11, 1493, 527, 345, 30]
        (Each number represents one token)
```

### Step 2: Model Processing
The model processes these token numbers:

```
Input: [9906, 11, 1493, 527, 345, 30]
  ↓ (through 96 transformer blocks)
  ↓
Output: Probability for next token

Most likely next tokens:
- "I" (20%)
- "I'm" (15%)
- "Let's" (10%)
```

### Step 3: Decoding
Converting tokens back to text:

```
Predicted token: 5210 → "I"
Text: "Hello, how are you? I"

Repeat: [original tokens] + [5210]
  ↓
Predict next token: 3445 → "am"

Text: "Hello, how are you? I am"
```

---

## Why You Pay Per Token

When you use an LLM API (ChatGPT, Claude, etc.), you pay based on **tokens used**:

```
Input: "Explain machine learning"  → Cost = # input tokens × input price
Output: [generated response]        → Cost = # output tokens × output price
Total cost = input + output

Example (Claude API):
- Input tokens: $0.80 per million
- Output tokens: $2.40 per million

For 1000 input tokens + 500 output tokens:
Cost = (1000 / 1,000,000) × $0.80 + (500 / 1,000,000) × $2.40
     = $0.0008 + $0.0012
     = $0.002
```

---

## Token Counting: The Practical Side

**Important:** Different models use slightly different tokenizers.

```
Model: GPT-4
Text: "Hello world!"
Tokens: 3

Model: Claude 3
Text: "Hello world!"
Tokens: 4

Same text, different number of tokens!
```

**Why?** Different training data, different tokenization algorithms.

### Real Examples

```
1. "AI is amazing"
   GPT-4: 4 tokens
   Claude: 5 tokens

2. "What is machine learning?"
   GPT-4: 6 tokens
   Claude: 7 tokens

3. This entire paragraph (~50 words)
   Probably: 75-100 tokens
```

**Rule of thumb:** ~1 token ≈ 0.75 words (English)

```
100 words ≈ 130 tokens
1000 words ≈ 1300 tokens
```

---

## Why Different Token Counts?

Different models have different vocabularies and tokenization strategies.

### Efficient Tokenization (Fewer Tokens)

```
Text: "Incredible"

Model A (has "incredible" in vocabulary):
- Encodes as: [1 token]

Model B (only has "incred" and "ible" in vocabulary):
- Encodes as: [2 tokens]

Model B has higher token cost!
```

### Language Variations

```
English: "the"        → 1 token
German: "der/die/das" → 1 token each (German uses more small words)
Japanese: "は"        → 1 token (but one character represents more meaning)
```

This is why non-English languages are often more expensive to use with LLMs.

---

## Context Window: The Maximum Length

LLMs have a **context window**: maximum number of tokens they can process at once.

```
Model          Context Window  Real-World
GPT-3.5 Turbo  4,096 tokens    ~3,000 words
GPT-4          8,192 tokens    ~6,000 words
Claude 3       200,000 tokens  ~150,000 words
GPT-4 Turbo    128,000 tokens  ~100,000 words
```

**What this means:**
- You can't ask GPT-3.5 to summarize a 100-page book (too many tokens)
- You can ask Claude to summarize a 100-page book (fits in context)

**Cost implication:**
- With Claude's 200K context, you send 200K tokens at once
- All 200K tokens count toward your bill

---

## Special Tokens

Some tokens have special meanings:

```
[BOS] = Beginning of Sequence
[EOS] = End of Sequence (model stops generating)
[PAD] = Padding (for alignment, not in API typically)
[UNK] = Unknown (rare word the tokenizer doesn't know)
<|im_start|> = Message start (in some models)
<|im_end|> = Message end
```

These are invisible to you, but they count toward token limits.

---

## Practical Examples

### Example 1: Asking a Question

```
Your input: "What is machine learning?"
Tokens: 5

Claude response (typical): 
"Machine learning is a branch of artificial intelligence..."
Tokens: 80

Total: 85 tokens
Your bill: (5 + 80) × [price per token]
```

### Example 2: Asking About a Document

```
Your input: "Summarize this document:\n\n[entire 10-page document]"
Document tokens: 3,000
Question tokens: 5
Total input: 3,005 tokens

Claude response (summary): ~200 tokens

Total: 3,205 tokens
Cost: Much higher because of the document!
```

### Example 3: Multi-turn Conversation

```
You: "What is AI?"     (5 tokens)
Claude: "AI is..." (50 tokens)

You: "Can you explain more?"  (5 tokens)
Claude: "Sure, AI involves..." (80 tokens)

You: "What about machine learning?"  (5 tokens)
Claude: "Machine learning is..." (100 tokens)

Turn 1: 5 input + 50 output = 55 tokens
Turn 2: 5 input + 80 output = 85 tokens  (doesn't repeat first turn)
Turn 3: 5 input + 100 output = 105 tokens

Wait, actually, the model sees the entire conversation history!
So Turn 3 actually sees all previous messages:
- Previous AI responses stay in context
- Your previous questions stay in context
- Only the new tokens are billed (usually)

Some APIs bill differently, so check!
```

---

## Token Optimization Tips

### 1. Be Concise
```
Bad: "Could you please, if it's not too much trouble, explain to me what machine learning is?"
Tokens: 25

Good: "What is machine learning?"
Tokens: 5

Savings: 20 tokens (4x reduction!)
```

### 2. Use Structured Input
```
Bad: "In a very complicated way, please explain machine learning in the context of artificial intelligence..."
Tokens: 30+

Good:
"Explain machine learning.
Context: AI
Audience: Beginner"
Tokens: 18

Savings: 12 tokens
```

### 3. Break Large Requests
```
Bad: Send 100K word document + question
Result: 100K+ tokens = expensive

Good: 
1. Summarize document first (in batches if needed)
2. Ask question about summary
Result: 10K tokens (after summary) = cheaper
```

### 4. Reuse Context Efficiently
```
One conversation (reuse context):
Turn 1: 100 tokens
Turn 2: 150 tokens (context remembered)
Turn 3: 200 tokens
Total: 450 tokens

Separate conversations (no context reuse):
Conv 1: 100 + 150 = 250 tokens
Conv 2: 200 tokens
Total: 450 tokens

Actually the same! But one conversation is better for coherence.
```

---

## Token Limits and What Happens

### Hard Limit
If you exceed the context window, the API rejects your request:

```
Your request: "Summarize this 500-page book: [text]"
Tokens needed: 150,000
Context window: 128,000

Error: "Request exceeds context window. Try breaking into smaller chunks."
```

### Soft Limit (Practical)
Even if you fit in the context window, using all of it is inefficient:

```
Context window: 8,192 tokens
Your input: 7,500 tokens
Available for output: 692 tokens

If the model starts generating a long response, it gets cut off!
```

### Best Practice
Use only 60-70% of context window:

```
Context window: 8,192 tokens
Safe limit: 5,000 tokens input
Reserved for output: 3,192 tokens

This prevents mid-response cutoffs.
```

---

## Advanced: How Tokenizers Work

Different tokenization algorithms:

### 1. Character-level
```
Text: "Hello"
Tokens: ['H', 'e', 'l', 'l', 'o'] = 5 tokens

Problem: Very long token sequences, but can handle any text
```

### 2. Word-level
```
Text: "Hello, how are you?"
Tokens: ['Hello', ',', 'how', 'are', 'you', '?'] = 6 tokens

Problem: Millions of unique words, including typos and rare words
```

### 3. Byte-Pair Encoding (BPE) - Used by Most LLMs
```
Step 1: Start with all characters as tokens
Step 2: Find most common pair of adjacent tokens
        "he" appears 1000 times
Step 3: Merge into single token: [he] = 1 token
Step 4: Repeat until vocabulary reaches desired size

Text: "hello"
Start: ['h', 'e', 'l', 'l', 'o']
After merging: ['he', 'll', 'o']
After more merging: ['hello'] = 1 token

This is why "hello" might be 1 token while "incredible" is 2 tokens!
```

---

## Self-Check

Can you answer:

- [ ] "What is a token?" (A piece of text, usually word or subword)
- [ ] "Why do LLMs charge per token?" (Token processing is metered, not flat-rate)
- [ ] "Is 'hello' always 1 token?" (Usually, but depends on the model and what's before it)
- [ ] "How many tokens in 'What is machine learning?'" (Around 5-6)
- [ ] "What's a context window?" (Maximum tokens the model can process at once)
- [ ] "If context is 8K tokens and your input is 7K, can you get a long response?" (No, only 1K left for output)

If you can answer these, you've completed **TIER 0: Absolute Fundamentals**! 🎉

**Next:** Move to [TIER-1-01-What-are-LLMs.md](TIER-1-01-What-are-LLMs.md) to learn how to actually use LLMs →
