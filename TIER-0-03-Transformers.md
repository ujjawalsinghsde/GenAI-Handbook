# TIER 0-03: Transformers
## The Architecture Behind Every Modern LLM

---

## Why Transformers Matter

Before Transformers (2017), training large language models was hard and slow.

After Transformers, it became possible to train models that could:
- Understand context (remember what happened earlier in a conversation)
- Process text in parallel (much faster training)
- Scale to billions of parameters (bigger = smarter)

**Result:** ChatGPT, Claude, LLaMA, all possible.

If you want to understand modern AI, you need to understand Transformers.

---

## The Problem They Solved

### Before Transformers: RNNs (Recurrent Neural Networks)

Imagine you're reading a sentence word by word:

```
"The bank executive walked into the bank to deposit money"
```

An RNN reads it like this:

```
Read "The" → Process
Read "bank" → Process using memory of "The"
Read "executive" → Process using memory of "The bank"
...
Read "bank" (second occurrence) → Process using memory of ALL previous words

But the memory degrades (fades) over long sequences
```

**Problem:** Remembering the first "bank" while processing the second "bank" is hard. The network forgets old information.

Also, it has to read word-by-word sequentially. Can't parallelize training.

### After Transformers: Attention

Transformers have a mechanism called **Attention** that lets the network ask:

"Wait, which words in this sentence are actually relevant to what I'm trying to predict?"

```
Predicting: "The bank executive walked into the ___ to deposit money"

Attention mechanism:
- "bank" (first one): 85% relevant (it's about banking)
- "executive": 60% relevant (who goes to a bank)
- "walked": 20% relevant (not important for this prediction)
- "money": 95% relevant (definitely relevant to banks)

Final prediction: The blank is probably "bank" because:
  - First "bank" is relevant
  - Context is about money/banking
```

**Why this matters:**
1. The network can directly "see" relevant information from anywhere in the text
2. No memory degradation over long sequences
3. Can process all words in parallel (much faster training)

---

## Attention Explained Simply

Let's use a real example: Reading a paragraph with pronouns.

```
"John walked into a store. He needed to buy milk. It was 9 PM. He rushed to the dairy section."
```

When you read "He needed to buy milk", you automatically know:
- "He" = John (from 2 words ago)
- "It" = the time (9 PM)

You don't re-read the entire paragraph. You just look at relevant parts.

**Attention does this for the network:**

```
At each word, the network asks: "Which other words should I pay attention to right now?"

Processing "milk":
  - Relevant: "store" (15% attention) - stores sell milk
  - Relevant: "needed" (25% attention) - about needing
  - Relevant: "buy" (50% attention) - he's buying it
  - Not relevant: "9" (0% attention) - time doesn't matter here

Result: Use 50% "buy" + 25% "needed" + 15% "store" to understand "milk"
```

That's Attention. At each step, the model decides what to pay attention to.

---

## The Transformer Block (High-Level)

Here's what happens inside a Transformer:

```
Input: "What is machine learning?"

1. TOKENIZATION
   "What" → [2034]
   "is" → [1034]
   "machine" → [3829]
   "learning" → [4521]

2. EMBEDDING
   [2034] → vector of 512 numbers representing "What"
   [1034] → vector of 512 numbers representing "is"
   (These vectors capture meaning - similar words are near each other)

3. ATTENTION
   For each word, figure out which other words to focus on
   "machine" pays attention to "learning" (they're related)
   "learning" pays attention to "machine" (related)
   "is" pays attention to "What" (grammatical relationship)

4. TRANSFORMER BLOCK
   Use the attention weights to combine information from relevant words
   Output: new representation of each word that includes context

5. FEED-FORWARD
   Pass through some neural network layers
   Output: Further refined representations

6. REPEAT
   Do steps 3-5 many times (12 layers, 24 layers, 96 layers depending on model size)

7. FINAL OUTPUT
   Last layer predicts: What's the next word most likely to be?
   Outputs probabilities for all 50,000 words in vocabulary
   "question" - 45%
   "is" - 30%
   "a" - 15%
   ...

Result: "machine learning?" → Next word is probably "question" (45% confident)
```

---

## Key Components Explained

### 1. Tokenization
Breaking text into pieces the model can understand:

```
Text: "ChatGPT is amazing"

Token-level:
"Chat" → token 1
"G" → token 2
"P" → token 3
"T" → token 4
"is" → token 5
"amazing" → token 6

(Note: Some words are 1 token, some are many tokens.
You pay per token, so this matters for cost!)
```

### 2. Embeddings
Converting tokens to vectors (lists of numbers):

```
"amazing" → [0.2, -0.5, 0.8, ..., 0.1]  (768 numbers for Claude)

These vectors are in "semantic space":
- Similar words are close to each other
- "amazing" is close to "incredible"
- "amazing" is far from "terrible"
```

### 3. Attention
The core mechanism. For each word, calculate:
- How much should I focus on other words?
- Which words are relevant to understanding this word?

```
Processing "learning" in "machine learning":

Query (what am I looking for?): "learning"
Keys (what words are available?): ["machine", "learning", ...]
Values (what info do they have?): [...embeddings...]

Attention = How relevant is each word?
- "machine" = 70% relevant
- "learning" = 30% relevant
- other words = 0% relevant

Result = 0.7 * embedding("machine") + 0.3 * embedding("learning")
       = Enhanced understanding of "learning" with "machine" context
```

### 4. Multi-Head Attention
Instead of asking once "which words should I focus on?", ask multiple times:

```
Head 1: "What words have the same grammatical function?"
        → Focuses on verbs if current word is a verb

Head 2: "What words have similar semantic meaning?"
        → Focuses on synonyms

Head 3: "What words are syntactically related?"
        → Focuses on subject/object relationships

Combine all heads → Rich understanding of context
```

This is why Transformers work so well. Multiple parallel attention heads each learn different relationships.

### 5. Feed-Forward Network
After attention, each representation goes through a simple neural network:

```
Attention output (vector) → Neural Network → Refined representation
```

This adds non-linearity and learns additional patterns.

---

## Why Transformers Are Powerful

### 1. Parallelization
Unlike RNNs that process sequentially (word 1, then word 2, then word 3):

```
RNN: Word 1 → Word 2 → Word 3 → Word 4 (takes 4x time)
Transformer: Process all words at once (same time as 1 word)
```

This is why modern models train so much faster.

### 2. Long Context
Attention solves the "memory fading" problem:

```
RNN: "What did the first word say?"
     After 10,000 words → Forgotten (fuzzy memory)

Transformer: "What did the first word say?"
             After 10,000 words → Can still see it clearly (direct attention)
```

### 3. Interpretability (Sort Of)
You can look at attention weights and see what the model focused on:

```
Input: "The cat sat on the mat"
Predicting next word...

Attention visualization:
"The" → pays attention to: "cat" (60%), "mat" (30%)
"sat" → pays attention to: "cat" (80%), "mat" (15%)

We can see the model is reasoning about relationships!
(Still a black box overall, but attention gives us hints)
```

---

## From Transformer Block to Full Model

One Transformer block processes text and passes it to the next block.

```
Input: "What is AI?"

Block 1: Learns basic patterns (tokens, simple meanings)
  ↓
Block 2: Learns word relationships
  ↓
Block 3: Learns sentence structure
  ↓
Block 4: Learns higher-level concepts
  ↓
...
Block 96: Learns complex reasoning and language patterns
  ↓
Output Layer: Predicts next token
```

**Stacking blocks** is what makes transformers deep and powerful.

More blocks = deeper understanding = better performance.

But also = more computation, longer training time, more parameters to store.

---

## Real Model Sizes

| Model | Blocks | Parameters | Training Time | Size |
|-------|--------|-----------|---------------|------|
| GPT-2 | 12 | 1.5B | Weeks | 6GB |
| GPT-3 | 96 | 175B | Months | 700GB |
| Claude 3 | ~80 | ~137B | Months | ~550GB |
| GPT-4 | Unknown | ~1.8T (estimated) | Months | ~2TB |

Bigger = more powerful, but exponentially more expensive to train and run.

---

## How LLMs Actually Generate Text

Now you understand Transformers. Here's how an LLM generates text:

```
1. Input: "Explain machine learning"
2. Tokenize: [explain], [machine], [learning]
3. Pass through transformer blocks (96 layers)
4. Output: Probability distribution over next token
   "in" - 30%
   "is" - 25%
   "simply" - 20%
   ...
5. Pick "in" (highest probability, or random if temperature=high)
6. Now input is "Explain machine learning in"
7. Repeat from step 3
8. Continue until model outputs [END] token

Result: Full explanation generated one token at a time
```

That's it. That's how ChatGPT writes responses.

---

## Attention is All You Need

The original Transformer paper (2017) was titled: "Attention is All You Need"

It showed:
- You don't need RNNs
- You don't need CNNs for text
- Attention (+ standard neural network layers) is enough

This was revolutionary. And it was right.

Every modern LLM is based on Transformers:
- ChatGPT
- Claude
- LLaMA
- Gemini
- All using the same core architecture from 2017

---

## Self-Check

Can you explain:

- [ ] "What problem did Transformers solve?" (Memory degradation in RNNs + slow sequential processing)
- [ ] "What is Attention?" (Mechanism to focus on relevant parts of input)
- [ ] "Why can Transformers process words in parallel?" (Because attention allows direct access to any word, not sequential)
- [ ] "What is a token?" (Piece of text, often a word or subword, you pay per token)
- [ ] "What does embedding do?" (Converts tokens to vectors in semantic space)
- [ ] "Why stack multiple blocks?" (Each block learns higher-level patterns)

If you got these, you're ready for **TIER 0-04: Tokens** (and why they cost money) →
