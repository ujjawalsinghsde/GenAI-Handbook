# TIER 1-02: How LLMs Generate Text
## The Step-by-Step Process

---

## The Simple Version

LLMs generate text **one token at a time**, like this:

```
1. You: "What is AI?"
2. Model processes and predicts: Next word is "AI" (most likely)
3. Output so far: "What is AI • "
4. Model uses that as new input, predicts: Next word is "stands" (most likely)
5. Output: "What is AI stands ..."
6. Keep repeating until [END] token

Result: Full response generated incrementally
```

That's why ChatGPT responses appear one word at a time on your screen—it's literally generating token by token.

---

## The Detailed Process

### Step 1: You Send a Prompt
```
Your prompt: "Explain machine learning in simple terms"
```

### Step 2: Tokenization
The model breaks your prompt into tokens:

```
"Explain" → [9283]
"machine" → [4521]
"learning" → [3847]
"in" → [627]
"simple" → [7492]
"terms" → [4185]

Token list: [9283, 4521, 3847, 627, 7492, 4185]
```

### Step 3: Embedding
Convert tokens to vectors (lists of numbers):

```
[9283] → [0.2, -0.5, 0.8, ..., 0.1] (768 dimensions for Claude)
[4521] → [0.1, 0.3, -0.2, ..., 0.5]
...
```

These vectors represent meaning. Similar concepts are near each other in this space.

### Step 4: Transformer Processing
Pass all embeddings through 96 transformer blocks (for Claude 3):

```
Block 1:
Input: [token embeddings]
Process: Attention + Feed-forward
Output: [refined embeddings]

Block 2:
Input: [output from Block 1]
Process: Attention + Feed-forward
Output: [more refined embeddings]

... (repeat 94 more times) ...

Block 96 (final):
Output: Representation of entire prompt with all context
```

Each block:
1. Looks at all tokens with attention (which tokens are relevant?)
2. Refines the representation based on what it focused on
3. Passes to the next block

### Step 5: Predicting the Next Token

After processing, the model has learned representations for the entire prompt.

It now asks: "Given this input, what's the most likely next token?"

Output: **Probabilities for all 50,000 tokens in vocabulary**

```
"Machine" → 0.15 (15% likely)
"learning" → 0.02 (2% likely)
"is" → 0.05 (5% likely)
"a" → 0.08 (8% likely)
"type" → 0.12 (12% likely)
"of" → 0.10 (10% likely)
[thousands of other tokens with small probabilities]

Sum = 1.0 (100% - they're probabilities)
```

### Step 6: Selecting the Next Token

The model chooses which token to output based on the probabilities.

**Method 1: Greedy (Always pick the most likely)**
```
Probabilities: "Machine" (15%), "type" (12%), "a" (8%)
Pick: "Machine" (highest)
```

This is deterministic. Same input always produces the same output.

**Method 2: Sampling (Random, weighted by probability)**
```
Probabilities: "Machine" (15%), "type" (12%), "a" (8%)
Pick: Random selection based on weights

Might pick "Machine" (most likely)
Might pick "type" (less likely, but possible)
Might pick "a" (rare, but could happen)
```

This adds randomness. Same input can produce different outputs.

**Method 3: Top-K Sampling (Only consider top K most likely)**
```
Probabilities: "Machine" (15%), "type" (12%), "a" (8%), ... (thousands more)
Only consider top 5: ["Machine" (15%), "type" (12%), "a" (8%), "kind" (6%), "category" (4%)]
Pick random from those 5, weighted by probability
```

This balances creativity with coherence.

### Step 7: Update the Context

Now you have one new token. Add it to the context and repeat:

```
Original tokens: [9283, 4521, 3847, 627, 7492, 4185]
Generated so far: []

Iteration 1:
Model predicts: Token [2891] ("Machine")
Generated: [2891]
New full context: [9283, 4521, 3847, 627, 7492, 4185, 2891]

Iteration 2:
Model sees: [9283, 4521, 3847, 627, 7492, 4185, 2891]
Predicts: Token [4521] ("learning")
Generated: [2891, 4521]
New full context: [9283, 4521, 3847, 627, 7492, 4185, 2891, 4521]

Iteration 3:
Model sees: [9283, 4521, 3847, 627, 7492, 4185, 2891, 4521]
Predicts: Token [1234] ("is")
Generated: [2891, 4521, 1234]
New full context: [9283, 4521, 3847, 627, 7492, 4185, 2891, 4521, 1234]

... (repeat until [END] token or max length reached) ...
```

### Step 8: Decoding

Convert generated tokens back to text:

```
Generated tokens: [2891, 4521, 1234, 627, 5847, ...]
Decode:
[2891] → "Machine"
[4521] → "learning"
[1234] → "is"
[627] → "a"
[5847] → "field"
...

Final text: "Machine learning is a field..."
```

---

## Visual Timeline

```
Time 0ms: You submit prompt
         ↓
Time 10ms: Tokenization complete
         ↓
Time 20ms: Embedding complete
         ↓
Time 50ms: All 96 transformer blocks processed
         ↓
Time 60ms: Predictions calculated (probabilities for all 50K tokens)
         ↓
Time 65ms: Token 1 selected and returned
         ↓
Time 100ms: Token 2 selected and returned
         ↓
Time 140ms: Token 3 selected and returned
         ↓
Time 180ms: Token 4 selected and returned
         ...
```

Each token takes ~40ms on average (varies by model and hardware).

A 100-token response takes roughly 4 seconds.

---

## Real Example

Let's trace through what actually happens:

**Your prompt:** "What is AI?"

### Tokenization
```
"What" → 1539
"is" → 372
"AI" → 9284
"?" → 30
```

### Through transformer (simplified)
```
Transformer sees: [1539, 372, 9284, 30]
Attention mechanism:
- "AI" pays attention to "What" (related)
- "is" pays attention to "What" and "AI" (linking them)
- Each token gets refined representation using all context
```

### Prediction
```
After 96 layers, model calculates:
"Artificial" → 0.25 (25%)
"The" → 0.15 (15%)
"It's" → 0.12 (12%)
"An" → 0.11 (11%)
...

Select: "Artificial" (25% is highest)
```

### Next iteration
```
New context: [1539, 372, 9284, 30, 5023] (where 5023 = "Artificial")
Model processes all 5 tokens through transformer again
Predicts next token...
```

### Continue until done
```
Generated tokens: [5023, 1928, 7384, 15, ...]
Decode: "Artificial Intelligence is the study of..."

Model generates until:
- [END] token appears
- OR max token limit reached
- OR you stop it (in chat, you can interrupt)
```

---

## Temperature: Controlling Randomness

When selecting the next token, we can adjust how "random" the model is:

### Low Temperature (e.g., 0.1)
Probabilities get squeezed. The highest probability gets even higher.

```
Original: "Machine" (15%), "type" (12%)
Squeezing: "Machine" (90%), "type" (9%)

Result: Almost always picks "Machine"
Response: Predictable, safe, deterministic
```

**Use case:** Factual questions where you want consistent, reliable answers.
```
Q: "What is the capital of France?"
A: "Paris" (always, every time)
```

### Medium Temperature (e.g., 0.7 - typical default)
Normal probability distribution.

```
Original: "Machine" (15%), "type" (12%), "a" (8%)
No change: "Machine" (15%), "type" (12%), "a" (8%)

Result: Some randomness, but focused on likely options
Response: Balanced between variety and coherence
```

**Use case:** Most normal conversation.

### High Temperature (e.g., 1.5)
Probabilities flatten. Lower-probability tokens become more likely.

```
Original: "Machine" (15%), "type" (12%), "a" (8%), "concept" (0.5%)
Flattened: "Machine" (8%), "type" (7%), "a" (6%), "concept" (5%)

Result: Much more randomness, even unlikely tokens appear
Response: Creative, varied, but sometimes nonsensical
```

**Use case:** Creative writing, brainstorming.
```
Prompt: "Start a story"
Output 1: "Once upon a time..."
Output 2: "In a dimension where..."
Output 3: "The purple elephant decided..."
(Each run is different)
```

---

## Top-P (Nucleus Sampling)

Instead of controlling how "extreme" probabilities are, you can control how many tokens to consider:

```
Top-P = 0.9: Only consider tokens that make up 90% of the cumulative probability

Probabilities (sorted):
"Machine" - 25% (cumulative: 25%)
"type" - 15% (cumulative: 40%)
"a" - 12% (cumulative: 52%)
"kind" - 10% (cumulative: 62%)
"field" - 8% (cumulative: 70%)
"or" - 8% (cumulative: 78%)
"concept" - 7% (cumulative: 85%)
"study" - 5% (cumulative: 90%) ← Stop here
[rest] - 10% (excluded)

Pick randomly from: Machine, type, a, kind, field, or, concept, study
```

**Effect:** Includes likely tokens, excludes very unlikely ones, but more natural than temperature.

---

## Why This Process Matters

### 1. Speed Implications
```
Generate 1 token: 40ms
Generate 10 tokens: 400ms (still fast)
Generate 100 tokens: 4 seconds (slow, but bearable)
Generate 1000 tokens: 40 seconds (very slow)

This is why long document generation feels slow!
```

### 2. Latency and Streaming
Because generation is sequential, users see text appearing gradually.

```
No streaming (wait for all tokens):
- User waits 4 seconds, then sees entire response at once

With streaming (show tokens as generated):
- User sees first token after 40ms
- User sees tokens trickling in
- Feels faster and more responsive (psychologically)
```

### 3. Cost Implications
```
Input: "Explain quantum physics" → 5 tokens (costs $X)
Output: 100-token explanation → 100 tokens (costs 100×$X)

Longer outputs = more expensive!

This is why you pay more for detailed answers than yes/no answers.
```

### 4. Error Compounding
Since each token depends on previous tokens, mistakes compound:

```
Correct generation:
"Machine learning is a field of AI"
(Each token correctly follows from previous ones)

Error generation (early mistake):
"Machine learning is an elephant"
(Early error: "elephant" instead of "field")

"An elephant jumps in"
(Next tokens now continue from the wrong context)
(Sentence becomes incoherent)
```

This is why models sometimes start well then go off the rails.

---

## Why This Matters for You

### For Users
Understanding this helps you debug why models produce weird outputs.

```
Q: "Why did ChatGPT suddenly switch topics?"
A: Because of token-by-token generation and compounding errors
   Early mistake → Next token is conditioned on wrong context → Entire response derails
```

### For Builders
Understanding this helps you:
1. Set appropriate temperature (creative vs deterministic)
2. Predict latency (more tokens = slower)
3. Optimize costs (fewer output tokens = cheaper)
4. Handle errors (early stopping, retry logic)

---

## Self-Check

Can you trace through:

- [ ] "How does an LLM generate text?" (One token at a time, using previous tokens as context)
- [ ] "What does temperature do?" (Controls randomness: low = deterministic, high = creative)
- [ ] "Why does long text generation take longer?" (More tokens to generate, and each token takes time)
- [ ] "Can a model fix mistakes once made?" (Hard - early mistakes compound into later errors)
- [ ] "What's the difference between Top-K and Top-P?" (Top-K: pick from K most likely; Top-P: pick from tokens making up P% of probability)

If you got these, you're ready for **[TIER-1-03-LLM-Parameters-Explained.md](TIER-1-03-LLM-Parameters-Explained.md)** →

Next document: Master the parameters that control LLM behavior.
