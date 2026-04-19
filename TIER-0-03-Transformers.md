# TIER 0-03: Transformers

## Table of Contents
1. [The Problem](#the-problem)
2. [The Core Idea: Attention](#the-core-idea-attention)
3. [How Attention Works (Detailed)](#how-attention-works-detailed)
4. [Multi-Head Attention](#multi-head-attention)
5. [The Feed-Forward Network](#the-feed-forward-network)
6. [Complete Step-by-Step Architecture](#complete-step-by-step-architecture)
7. [What Happens After Transformation](#what-happens-after-transformation)
8. [Putting It All Together](#putting-it-all-together)
9. [Why Transformers Changed Everything](#why-transformers-changed-everything)

---

## The Problem

**Before Transformers (before 2017):**
- AI models read text like you'd read with your finger — **one word at a time, left to right**
- By the time they got to word 50, they'd mostly forgotten word 1
- Long sentences were hard. Long documents were nearly impossible.
- Different models were needed for different tasks (one for text, one for images, one for audio)

**Example of the problem:**
If a model reads: "The trophy didn't fit in the bag because it was too big"

By the time it reaches the word "it" at the end, it might have forgotten what "the" and "trophy" mean. It can't properly figure out whether "it" refers to the trophy or the bag.

**The Solution:**
Transformers throw out the sequential reading idea entirely. Instead, they look at **every word at the same time** and let every word "talk to" every other word to figure out what each one means in context.

---

## The Core Idea: Attention

### What Is Attention?

Attention is the mechanism that lets the model understand relationships between words.

**Real-world example:**
When you read "The trophy didn't fit in the bag because it was too big" — your brain instantly connects:
- "it" → "trophy" (not the bag)
- "was too big" → explains why it didn't fit
- "didn't fit" is the main action

You do this by **paying attention to** the relevant words. Your brain doesn't process "the" or "in" deeply — it focuses on the important connections.

**That's exactly what Attention does:**
For every word, it calculates how much it should "pay attention" to every other word to understand what that word means.

### The Intuition: A Voting System

Think of Attention as a democratic voting process:

1. Every word in the sentence raises its hand and asks: **"What other words should I pay attention to?"**
2. Every other word votes on whether they're relevant
3. The votes are counted
4. Each word collects the "winner" words to better understand itself

**Simple example:**
```
Sentence: "The cat chased the tail quickly"

Word "chased" asks: "Who is doing the chasing? What is being chased?"
- "cat" votes: "I'm relevant! I'm the one doing the chasing!"
- "tail" votes: "I'm relevant! I'm what's being chased!"
- "quickly" votes: "I'm somewhat relevant! I describe how it happened!"
- "the" votes: "I'm not very relevant..."

Result: "chased" now has a rich understanding that blends information about
"cat", "tail", "quickly", and barely touches "the"
```

---

## How Attention Works (Detailed)

### The Three Key Concepts: Query, Key, Value

For each word, the Transformer creates **three things**. Think of it like a library system:

#### Query (Q) — "What am I looking for?"
- This is the question a word is asking
- For "chased": *"Who is doing the chasing? What is being chased?"*
- For "the": *"What thing am I describing?"*
- It's a vector (a list of numbers) that encodes the word's "question"

#### Key (K) — "Here's what I contain"
- This is what each word broadcasts about itself
- "cat" broadcasts: *"I'm a subject, a noun, a singular animal"*
- "tail" broadcasts: *"I'm an object, a noun, a body part"*
- "quickly" broadcasts: *"I'm an adverb, a descriptor"*
- It's a vector that summarizes what the word offers

#### Value (V) — "Here's my actual content"
- This is the actual meaning/content of the word
- When another word decides you're relevant, they get access to your Value
- It's a vector containing the word's full semantic information

### The Step-by-Step Process

**Step 1: Match Query against all Keys**

The model calculates how well each word's Question (Query) matches every word's Label (Key).

```
"chased" (Query) vs:
- "cat" (Key):        90% match (very relevant)
- "tail" (Key):       85% match (very relevant)
- "quickly" (Key):    50% match (somewhat relevant)
- "the" (Key):         5% match (not relevant)
- "chased" (Key):     70% match (somewhat relevant)
```

This matching is done with a mathematical operation: we multiply the Query vector by each Key vector and get a similarity score.

**Step 2: Convert Scores to Percentages (Softmax)**

The model converts these scores into percentages that add up to 100%, using a mathematical function called Softmax.

```
- "cat":       35% of attention
- "tail":      32% of attention
- "chased":    18% of attention
- "quickly":   12% of attention
- "the":        3% of attention
(Total = 100%)
```

**Step 3: Collect Values Weighted by Attention**

Now the model collects each word's Value, weighted by how much attention that word deserves.

```
New representation of "chased" = 
  (0.35 × cat's Value) + 
  (0.32 × tail's Value) + 
  (0.18 × chased's Value) + 
  (0.12 × quickly's Value) + 
  (0.03 × the's Value)
```

This creates a blend — mostly cat and tail (because they're most relevant), some of chased and quickly, barely anything from "the".

**Step 4: Output the Result**

The result is a new, richer vector for "chased" that carries information about:
- What animal is doing the chasing (cat)
- What is being chased (tail)
- How it's happening (quickly)
- All in one vector

This new vector replaces the old one and goes to the next layer of processing.

### Why This Matters

Before attention, "chased" was just one generic vector. After attention, it's a **context-aware** vector that understands its role in the sentence. That's the breakthrough.

---

## Multi-Head Attention

### The Problem with Single Attention

One attention mechanism looking at one relationship at a time isn't enough. A sentence has many different kinds of relationships happening simultaneously:

- Grammar relationships (subject/verb/object)
- Who is doing what to whom
- What words refer to the same thing (co-references)
- Cause and effect relationships
- Timing relationships

Trying to capture all of these through one attention lens would confuse the model. It's like reading a book for plot, character development, writing style, and historical context all at exactly the same time.

### The Solution: Multiple Heads

**Multi-Head Attention runs many attention mechanisms in parallel** — each one looking at relationships from a different angle.

Think of it like **reading the same sentence with different colored highlighters**:

```
Sentence: "The cat chased the tail quickly"

Head 1 (Grammar) highlights:
- Subject: cat
- Verb: chased
- Object: tail

Head 2 (Co-reference) highlights:
- "The" (first) points to: cat
- "The" (second) points to: tail
- "it" would point to: tail (if it were there)

Head 3 (Attributes) highlights:
- "cat" modified by: "the"
- "chased" modified by: "quickly"
- "tail" modified by: "the"

Head 4 (Semantics) highlights:
- "cat" = agent
- "chased" = action
- "tail" = patient
```

Each head independently performs attention, producing its own output. Then all outputs are stitched together.

### How Many Heads?

- Small models: 8 heads
- Medium models (like GPT-2): 12 heads
- Large models (like GPT-3): 96 heads
- Claude: 100+ heads

More heads = more perspectives = richer understanding, but also slower and uses more memory.

### The Mathematical View

```
Multi-Head Attention = Combine(Head1, Head2, Head3, ..., HeadN)

Each Head performs:
Output = Softmax(Query × Key^T / √(key_dimension)) × Value

Then all outputs are concatenated:
Combined = [Head1_output || Head2_output || Head3_output || ...]

Finally, a learned projection transforms this back to the original size
Final_output = Combined × Projection_matrix
```

(Don't worry if this looks complex — the key point is that each head does the same operation independently, then results are combined)

---

## The Feed-Forward Network

### What Comes After Attention?

After attention has happened, each word has gathered information from all other words. Now the model needs to **think about and process that information**.

That's where the feed-forward network comes in.

### The Analogy: From Gathering to Processing

Imagine attention is a researcher going to the library and collecting books on a topic. The feed-forward network is the researcher sitting at their desk, actually **reading, synthesizing, and thinking** about those books to write a final report.

Attention = gathering information  
Feed-forward = thinking about that information

### What's Inside the Feed-Forward Network

The feed-forward network is surprisingly simple — it has 3 steps:

**Step 1: Expand (Make it bigger)**
```
Input vector: 768 numbers
↓ (multiply by weights)
Expanded vector: 3,072 numbers (4× bigger)
```

**Step 2: Apply ReLU (Filter out noise)**

ReLU is incredibly simple:
```
if number < 0:
    set it to 0
else:
    keep it as is
```

Why? Because without this, every layer just does multiplication and addition (linear math). Linear math stacked on top of linear math is still linear — the network could never understand complex patterns.

ReLU **breaks linearity** by making some signals pass through and killing others. It's like a bouncer at a nightclub — some information gets in (positive values), some gets turned away at the door (negative values become zero).

**Step 3: Compress back down**
```
After ReLU: 3,072 numbers
↓ (multiply by different weights)
Output vector: 768 numbers
```

### Why Expand 4× First?

Why not just stay at 768 the whole time?

**Analogy:** Imagine sorting 100 random objects into categories. It's hard in a tiny room. But if you spread everything out on a huge table first, you can see patterns, remove duplicates, and regroup — then pack only the important findings back into a small box.

The expansion gives the network more computational space to:
- Find complex patterns
- Combine information in creative ways
- Filter out irrelevant information

The compression packs only the important findings back into the output.

### Attention vs Feed-Forward: The Key Difference

| Aspect | Attention | Feed-Forward |
|--------|-----------|--------------|
| **What it does** | Gathers information from other words | Processes information independently |
| **Who it talks to** | All other words | Nobody — works alone on each word |
| **Real-world analogy** | Going to the library | Sitting at your desk thinking |
| **Input** | Word vectors | Word vectors (context-aware from attention) |
| **Output** | Context-enriched vectors | Deeper, more processed vectors |
| **Works independently?** | No (needs other words) | Yes (processes each word alone) |

### The Summary

Feed-forward = **"Let me think deeply about what I just learned from the rest of the sentence"**

---

## Complete Step-by-Step Architecture

Now let's walk through the entire Transformer architecture from raw text to output.

### Step 1: Tokenization

**What happens:** Text is converted into numbers.

```
Input text: "Hello world"
           ↓
Tokenize: ["Hello", "world"]
           ↓
Convert to IDs: [15496, 995]
           ↓
The model only works with numbers from now on
```

**Why:** Neural networks can only work with numbers. There's no such thing as a word "Hello" to a neural network — only numbers.

**How it works:**
- The model has a vocabulary of ~50,000 words
- Each word (or subword) gets a unique number
- If a word is rare, it gets broken into subword pieces
- Special tokens are added (start token, end token, padding tokens)

---

### Step 2: Embedding Layer

**What happens:** Numbers are converted into meaningful vectors.

```
Token ID: 15496 (the word "hello")
           ↓
Look up in embedding table
           ↓
Embedding vector: [0.23, -0.5, 0.88, ..., 0.14] (768 numbers)
```

**What this means:**
- Each token ID is converted into a **dense vector** (a list of 768 numbers)
- These numbers were learned during training and represent the meaning of the word
- Similar words have similar vectors (close to each other mathematically)
- Words that can substitute for each other have nearly identical vectors

**Example:**
```
Embedding of "cat":     [0.2, -0.1,  0.5, ...]
Embedding of "dog":     [0.19, -0.09, 0.51, ...]  ← very similar!
Embedding of "quickly": [-0.3, 0.7, -0.2, ...]   ← very different!
```

---

### Step 3: Positional Encoding

**The problem:** Attention processes all words at the same time, so it doesn't inherently know word order.

Example: "Dog bites man" vs "Man bites dog" would look identical to the model without position info.

**The solution:** Add position information to each word's vector.

```
Token embedding:        [0.23, -0.5, 0.88, ..., 0.14]
Add position encoding:  [0.01, 0.99, 0.02, ..., 0.45]  ← encodes: "position 2"
                        ────────────────────────────────
Result:                 [0.24, 0.49, 0.90, ..., 0.59]
```

**How position encoding works:**
- Words at position 0 get one pattern of numbers
- Words at position 1 get a different pattern
- Words at position 2 get yet another pattern
- And so on...

The model learns to recognize these patterns and understand "word order."

---

### Step 4: Multi-Head Attention Layer

**What happens:** Each word looks at all other words and figures out which ones are relevant to understanding itself.

```
Input: Embedded & positioned word vectors
           ↓
Split into multiple attention heads (8, 12, 96, etc.)
           ↓
For each head:
- Generate Query, Key, Value for each word
- Score each word's Query against all Keys
- Weight each word's Value by attention scores
- Output: refined, context-aware vector
           ↓
Concatenate all head outputs
           ↓
Project back to original size (768 dimensions)
           ↓
Output: All words now have context from all other words
```

**What changed:**
- "the" now knows it's describing something upcoming
- "cat" now understands it's the subject doing an action
- "chased" now knows who is chasing whom
- "tail" now knows it's being chased

---

### Step 5: Feed-Forward Network

**What happens:** Each word's vector (independently) gets deeper thinking.

```
Input: [0.24, 0.49, 0.90, ..., 0.59]  (768 numbers)
           ↓
Expand to 3,072 numbers
           ↓
Apply ReLU (kill negative numbers, keep positive)
           ↓
Compress back to 768 numbers
           ↓
Output: [0.18, 0.52, 0.87, ..., 0.61]
```

**What happened:**
- The vector was transformed through non-linear operations
- Patterns and relationships were discovered
- Irrelevant information was filtered out
- The result is a deeper, more thoughtful representation

---

### Step 6: Residual Connection & Layer Normalization

**Two important things happen here:**

#### Residual Connection
```
Input vector:  [0.24, 0.49, 0.90, ..., 0.59]
Feed-forward output: [0.18, 0.52, 0.87, ..., 0.61]
                ↓
Result = Input + Feed-forward output
       = [0.42, 1.01, 1.77, ..., 1.20]
```

**Why:** This keeps information from earlier in the network from being lost. If the feed-forward output is wrong or noisy, the original input is still there to fall back on.

#### Layer Normalization
```
[0.42, 1.01, 1.77, ..., 1.20]
        ↓
Normalize so mean = 0, variance = 1
        ↓
[stable vector for next layer]
```

**Why:** This keeps the numbers stable as they flow through the network, preventing numerical problems.

---

### Step 7: Repeat (Stacking Layers)

Steps 4, 5, 6 form one **Transformer block**. The model stacks many of these.

```
Input text
    ↓
Block 1: Attention + Feed-forward
    ↓ (refined representation)
Block 2: Attention + Feed-forward
    ↓ (more refined)
Block 3: Attention + Feed-forward
    ↓ (even more refined)
... (many more blocks)
    ↓
Block 96: Attention + Feed-forward
    ↓ (final, deeply processed representation)
Output layer
```

**What's happening in each layer:**

- **Early blocks (1-10):** Learning grammar, syntax, simple patterns ("subject then verb")
- **Middle blocks (10-50):** Learning semantic relationships (what words mean together)
- **Late blocks (50-96):** Learning complex reasoning, facts, relationships, and world knowledge

Each layer builds on the previous one, creating increasingly sophisticated representations.

**Example — understanding "The trophy didn't fit in the bag because it was too big":**

- Block 1: Recognizes sentence structure (subject, verb, object)
- Block 5: Understands "didn't fit" is describing a relationship
- Block 20: Understands "because" introduces explanation
- Block 50: Understands "it" is a pronoun that needs resolution
- Block 96: Connects "it" to "trophy" (not "bag"), understands why

---

### Step 8: Output Layer

**What happens:** The final vector is converted into probabilities for the next word.

```
Final hidden vector: [0.18, 0.52, 0.87, ..., 0.61]  (768 numbers)
              ↓
Multiply by output projection matrix
              ↓
Probability distribution: [0.02, 0.15, 0.001, ..., 0.04]
(one score for each of ~50,000 words in vocabulary)
              ↓
Top predictions:
- "is" (8%)
- "was" (6%)
- "becomes" (2%)
- etc.
```

**What this means:**
The model has computed the probability of every possible next word. Usually, it picks the highest probability word, but it can also:
- **Sample** from the top candidates for variety
- **Adjust temperature** (how confident it is about picking the top choice)
- **Use beam search** (explore multiple possibilities)

---

## What Happens After Transformation

### After the First Token

Once the model outputs the first token, something crucial happens:

```
Original input: "Hello"
                ↓
Output: "world" (or other next word)
                ↓
Now input becomes: "Hello world"
                ↓
Run the entire Transformer again
                ↓
Output: next word (e.g., "is")
                ↓
Input becomes: "Hello world is"
```

**This continues until:**
- The model outputs an end-of-sequence token
- A maximum length is reached
- Manual stop signal

### Text Generation Process

```
Step 1: Input = "Hello"
        Process through Transformer
        Output prediction: "world" (35% confidence)
        
Step 2: Input = "Hello world"
        Process through Transformer
        Output prediction: "is" (42% confidence)
        
Step 3: Input = "Hello world is"
        Process through Transformer
        Output prediction: "a" (58% confidence)
        
Step 4: Input = "Hello world is a"
        Process through Transformer
        Output prediction: "beautiful" (22% confidence)
        
... continues until it outputs a stop token or reaches max length
```

### Decoding Strategies

After the model outputs probabilities, several strategies can pick the next word:

#### 1. Greedy Decoding
**Pick the highest probability word**
```
Probabilities: [is: 0.42, was: 0.38, are: 0.15]
Choose: "is" (highest)
```
**Pro:** Always picks the "best" next word  
**Con:** Can get stuck in repetitive loops; sometimes misses better paths

#### 2. Random Sampling
**Randomly pick from all words, weighted by probability**
```
Probabilities: [is: 0.42, was: 0.38, are: 0.15]
Random pick from distribution: "was" (sampled randomly)
```
**Pro:** More creative/diverse output  
**Con:** Can pick bad words; output can be nonsensical

#### 3. Top-K Sampling
**Only consider the top K words, then randomly sample**
```
All words: 50,000 options
Top-5: [is: 0.42, was: 0.38, are: 0.15, be: 0.03, has: 0.01]
Random pick from top-5: "are"
```
**Pro:** Diverse but sensible  
**Con:** Slower (need to sort)

#### 4. Beam Search
**Keep multiple possibilities alive and pick the best path**
```
Step 1: Keep top 3: "is", "was", "are"
Step 2: For each, generate top 3 next words
        - "is" → top 3 continuations
        - "was" → top 3 continuations
        - "are" → top 3 continuations
Step 3: Pick the complete path with highest total probability
```
**Pro:** Finds best path overall (not just next word)  
**Con:** Much slower; memory intensive

### Multiple Passes Through the Network

Important to understand: **The entire Transformer runs for each token generated.**

For an output of 100 words:
- Run 1: Input 1 token → output next token
- Run 2: Input 2 tokens → output next token
- Run 3: Input 3 tokens → output next token
- ...
- Run 100: Input 100 tokens → output next token

**This is slow!** But this is also why the model can be so careful — it reconsidering everything at each step.

(Note: In practice, optimizations like KV-cache speed this up dramatically by not recomputing attention for previous tokens)

---

## Putting It All Together

### The Complete Flow: Input to Output

```
RAW TEXT INPUT
     │
     ├─→ Tokenization: "Hello world" → [15496, 995]
     │
     ├─→ Token Embedding: [15496, 995] → vectors of 768 numbers
     │
     ├─→ Add Position Info: Mark which word is at which position
     │
     └─→ TRANSFORMER BLOCKS (stacked 12-96 times)
          │
          ├─→ Block 1:
          │    ├─ Multi-Head Attention (8-100 heads)
          │    │  └─ Each word looks at all others
          │    ├─ Feed-Forward Network
          │    │  └─ Deeper thinking on each word
          │    └─ Add residual connection & normalize
          │
          ├─→ Block 2:
          │    ├─ Multi-Head Attention
          │    ├─ Feed-Forward
          │    └─ Add residual & normalize
          │
          ├─→ Block 3: ... (same)
          │
          └─→ Block N: (final block)
               └─ Output: Deeply processed vectors
                
     ├─→ Output Layer: Convert to 50,000 word probabilities
     │
     └─→ SELECT NEXT WORD
          └─ Greedy, sample, beam search, etc.
     
     └─→ IF NOT END TOKEN, LOOP BACK WITH NEW INPUT

```

### A Concrete Example

**Let's trace one word through the entire system:**

```
Original sentence: "The cat chased the tail quickly"
Focus word: "chased"

────────────────────────────────────────────────────────────

STEP 1: TOKENIZATION
"chased" → Token ID: 2901

────────────────────────────────────────────────────────────

STEP 2: EMBEDDING
Token 2901 → [0.23, -0.5, 0.88, 0.12, ..., 0.14]  (768 dims)

────────────────────────────────────────────────────────────

STEP 3: POSITION ENCODING
Position 2 → [0.01, 0.99, 0.02, ..., 0.45]
Combined → [0.24, 0.49, 0.90, ..., 0.59]

────────────────────────────────────────────────────────────

STEP 4-6: BLOCK 1 (Attention + Feed-forward)
Input: [0.24, 0.49, 0.90, ..., 0.59]

Attention Stage:
- "chased" generates Query: "Who is doing what?"
- All words broadcast their Keys
- "cat" (Key) matches high with "chased" (Query) → 35% attention
- "tail" (Key) matches high → 32% attention
- "quickly" (Key) matches → 12% attention
- Other words get lower attention

- Collect Values weighted by attention
- Result: "chased" now has info about cat, tail, quickly

Output after Block 1: [0.22, 0.51, 0.85, ..., 0.58]
(Slightly different — it now knows about cat/tail/quickly)

────────────────────────────────────────────────────────────

STEP 4-6: BLOCK 2
Input: [0.22, 0.51, 0.85, ..., 0.58]
(Same process, but building on Block 1's output)

Attention Stage:
- Now "chased" asks deeper questions with better context
- Connections to other words get refined
- Understanding deepens

Output after Block 2: [0.20, 0.53, 0.84, ..., 0.60]

────────────────────────────────────────────────────────────

... (repeat for blocks 3, 4, 5... up to 96)

────────────────────────────────────────────────────────────

FINAL OUTPUT after Block 96: [0.18, 0.52, 0.87, ..., 0.61]

At this point, this vector represents "chased" with:
- Full understanding of sentence structure
- Clear connection to "cat" (subject)
- Clear connection to "tail" (object)
- Understanding that it happened in past tense
- Understanding that it happened quickly
- All relationships in the sentence
- Knowledge about causality (why anything chased anything)

────────────────────────────────────────────────────────────

STEP 8: OUTPUT LAYER
Final vector [0.18, 0.52, 0.87, ..., 0.61]
    ↓
Multiply by output weights
    ↓
Probability for each of 50,000 words:
- "quickly" (after "chased the tail"): 8%
- "her" (object): 6%
- "the" (article): 2%
- etc.

────────────────────────────────────────────────────────────

DECODING:
The model has now computed: "The cat chased ___"
It picks next word based on probabilities
Output: "the tail" (or other continuation)

The process repeats for the next token...
```

---

## Why Transformers Changed Everything

### Before Transformers
| Task | Architecture | Status |
|------|--------------|--------|
| Text generation | RNN/LSTM | Okay, but slow and forgot long context |
| Image recognition | CNN | Good, but couldn't handle text |
| Speech | Different model | Completely separate architecture |
| Translation | Separate model | Different from everything else |

**Problem:** You needed a different AI architecture for each problem. They didn't transfer knowledge between tasks.

### After Transformers

**The same Transformer architecture works for almost everything:**

| What you want | Model | Based on |
|---|---|---|
| Write and chat | GPT-4, Claude 3 | Transformer |
| Generate images | DALL-E 3, Stable Diffusion | Transformer-based |
| Translate languages | Google Translate | Transformer |
| Write code | GitHub Copilot, Claude | Transformer |
| Speech recognition | OpenAI Whisper | Transformer-based |
| Protein structure | AlphaFold 2 | Transformer-based |
| Play games | AlphaStar | Transformer-based |

**Why?** Because Attention is completely general. It works on any sequence of anything:
- Words? Yes → Language models
- Pixels? Yes → Image models
- Audio frames? Yes → Speech models
- Amino acids? Yes → Protein models
- Game positions? Yes → Game AI

You just change what the tokens represent.

### The Key Advantages of Transformers

| Advantage | Why It Matters |
|-----------|----------------|
| **Processes all words at once** | Can understand long-range dependencies (word 1 connects to word 100) |
| **Parallel computation** | Can be computed on GPUs/TPUs much faster than sequential models |
| **Transfer learning works** | Train on one task, fine-tune on another |
| **Scales well** | Bigger models are better (unlike older architectures) |
| **Attention is interpretable** | You can see which words the model paid attention to |
| **General mechanism** | Works for text, images, audio, and more |

---

## Summary and Key Takeaways

### The Essence of Transformers

**In one sentence:**  
A Transformer reads everything at once, lets every piece of information attend to every other piece through multiple parallel perspectives, processes that information deeply through feed-forward networks, repeats this many times through stacked layers, and outputs a probability over what should come next.

### The Three Core Insights

1. **Attention is powerful:** Letting each word "look at" every other word (rather than sequential processing) solves the context problem.

2. **Multi-head attention is crucial:** Different aspects of language need different attention patterns. Running them in parallel captures all of them.

3. **Stacked layers build sophistication:** Early layers learn simple patterns, late layers learn complex reasoning. Deeper networks understand deeper concepts.

### The Main Phases of Processing

```
Tokenization & Embedding
        ↓
Position Encoding
        ↓
Stacked Transformer Blocks (each block has):
├─ Multi-Head Attention (gather context from all words)
├─ Feed-Forward Network (think deeply about that context)
└─ Residual Connection & Normalization (keep info, stabilize)
        ↓
Output Layer
        ↓
Next Word Prediction
        ↓
If not done, repeat with new input (autoregressive generation)
```

### What Makes Transformers Revolutionary

Before Transformers: Different architectures for different problems, struggle with long-range dependencies, sequential processing.

After Transformers: One architecture for everything, handles long-range dependencies effortlessly, massive parallelization, scales to billions of parameters.

---

## Glossary of Terms

| Term | Simple Explanation |
|------|-------------------|
| **Token** | A piece of text (word, subword, or character) converted to a number |
| **Embedding** | Converting a number (token ID) into a meaningful vector of 768+ numbers |
| **Vector** | A list of numbers (like coordinates in high-dimensional space) |
| **Attention** | A mechanism for deciding which parts of input are important |
| **Query** | What a word is asking or looking for |
| **Key** | What a word broadcasts about itself |
| **Value** | What a word offers when selected |
| **Softmax** | Math function that converts scores into percentages (0-100%) |
| **Transformer Block** | One layer of Attention + Feed-Forward + Normalization |
| **Residual Connection** | Adding input back to output so information isn't lost |
| **Layer Normalization** | Keeping numbers stable as they flow through layers |
| **Feed-Forward Network** | Non-linear processing applied independently to each word |
| **ReLU** | Function that kills negative numbers, keeps positive ones |
| **Greedy Decoding** | Picking the highest probability word at each step |
| **Beam Search** | Exploring multiple possibilities to find the best overall path |
| **Autoregressive** | Generating one token at a time, with each token becoming part of the next input |

---

## Final Thoughts

Transformers are genuinely revolutionary, but they're built from simple ideas:
1. **Attention** — let everything look at everything
2. **Multi-perspective** — do this many times with different lenses
3. **Deep processing** — stack layers so understanding becomes sophisticated
4. **Repetition** — generate one token at a time, always rechecking everything

The "magic" isn't really magic — it's just these simple ideas, applied thoughtfully, at massive scale, trained on billions of examples.

Once you understand these core ideas (which you do now!), you've understood the fundamental mechanism behind GPT, Claude, DALL-E, and most of modern AI.

---

**End of Guide**

Feel free to re-read sections that were confusing. The key is to understand the flow:
- Text → Numbers (Tokenization & Embedding)
- Gather Context (Attention)
- Think Deeply (Feed-Forward)
- Repeat Many Times (Stacked Blocks)
- Output (Probability for Next Word)
- Repeat for Each Generated Word (Autoregressive)

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
