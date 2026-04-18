# TIER 1-03: LLM Parameters Explained
## Temperature, Max Tokens, and What They Do

---

## The Three Most Important Parameters

When you call an LLM API, you control how it behaves with parameters:

```python
# Example API call
response = claude.messages.create(
    model="claude-3-sonnet",
    max_tokens=1000,        # Parameter 1
    temperature=0.7,        # Parameter 2
    top_p=0.95,            # Parameter 3
    messages=[...]
)
```

Let's understand what each does and when to use them.

---

## 1. Temperature (Randomness)

**What it is:** How "creative" or "random" the model is.

**Range:** 0 to 2 (but typically 0 to 1)

**Default:** Usually 0.7 (balanced)

### Temperature = 0
**Behavior:** Deterministic. Always picks the highest probability token.

```
Probabilities: "Machine" (25%), "type" (15%), "a" (8%)
Picks: Always "Machine"
```

**When to use:**
- Factual Q&A (want correct, consistent answers)
- Data extraction (want reproducible results)
- Code generation (want working code, not random variations)

**Example:**
```
Q: "What's the capital of France?"
Temp 0: Always "Paris"
```

### Temperature = 0.5
**Behavior:** Slightly random. Focused on likely tokens but not rigid.

```
Mostly picks high-probability tokens, but occasionally picks medium ones
```

**When to use:**
- Most professional use cases
- Customer service bots
- When you want reliability with slight variety

### Temperature = 1.0 (Default for many models)
**Behavior:** Normal randomness. Follows probability distribution naturally.

```
Probabilities: "Machine" (25%), "type" (15%), "a" (8%), "concept" (1%)
Picks: Randomly weighted toward "Machine", but might pick others
```

**When to use:**
- General conversation
- Most use cases where you're uncertain
- Good balance of coherence and variety

**Example:**
```
Q: "Suggest a story title"
Temp 1.0:
Run 1: "The Last Robot"
Run 2: "Digital Dreams"
Run 3: "Synthetic Minds"
```

### Temperature = 1.5+
**Behavior:** Very random. Even unlikely tokens might appear.

```
Low-probability tokens now have significant chance of being selected
```

**When to use:**
- Creative brainstorming (poetry, art, ideas)
- Generating multiple diverse options
- When you want unexpected outputs

**Warning:** Can produce nonsensical text. Use carefully.

---

## 2. Max Tokens (Output Length)

**What it is:** Maximum number of tokens the model can generate.

**Range:** Any positive number, up to the context window

**Default:** Often 1000-2000, or unlimited

### Examples

```
max_tokens=10:
"This is a short response with fewer words in total."

max_tokens=100:
"This is a much longer response. The model can explain more details, provide examples, and give a more thorough answer to your question. It can go into depth on the topic."

max_tokens=1000:
[Can generate essays, code examples, detailed explanations]

max_tokens=10000:
[Can generate books, long documents, comprehensive analyses]
```

### Why It Matters

**Cost:**
```
More tokens = higher cost
Input: 500 tokens = $X
Output with max_tokens=100: ~$0.24X
Output with max_tokens=1000: ~$2.4X
```

**Response Time:**
```
More tokens = longer wait time
Generating 10 tokens: ~400ms
Generating 100 tokens: ~4 seconds
Generating 1000 tokens: ~40 seconds
```

### When to Use Different Limits

```
max_tokens=50:   Short answers only (Q&A, classification)
max_tokens=500:  Medium answers (explanations, summaries)
max_tokens=1000: Long answers (detailed explanations, code)
max_tokens=4000: Very long (multi-paragraph essays)
Unlimited:       Let model stop naturally
```

### The Cutoff Problem

If the model hits max_tokens while generating, it stops mid-response:

```
Your prompt: "Write a 500-word essay about AI"
max_tokens=100

Output (gets cut off):
"AI is transforming the world. It's used in healthcare, finance, and technology. 
The impact is significant, but there are also challenges. 

First, the benefits include..."

[Response stops here, essay is incomplete]
```

To avoid this, set max_tokens higher than you expect the response to be.

---

## 3. Top-P (Nucleus Sampling)

**What it is:** Cumulative probability threshold. Include tokens up to this probability.

**Range:** 0 to 1

**Default:** Usually 1.0 (consider all tokens)

### How It Works

```
All tokens and their probabilities (sorted highest to lowest):
"Machine" - 25%
"type" - 15%
"a" - 12%
"kind" - 10%
"field" - 8%
"or" - 8%
"concept" - 7%
"study" - 5%
"system" - 3%
[remaining tokens] - 7%

With top_p=0.9:
Include tokens until cumulative probability reaches 90%:
- "Machine" (25%): cumulative = 25%
- "type" (15%): cumulative = 40%
- "a" (12%): cumulative = 52%
- "kind" (10%): cumulative = 62%
- "field" (8%): cumulative = 70%
- "or" (8%): cumulative = 78%
- "concept" (7%): cumulative = 85%
- "study" (5%): cumulative = 90% ✓ STOP

Only pick from these 8 tokens. Ignore the rest.
```

### Temperature vs. Top-P

**Temperature:** Adjusts how extreme probabilities are

**Top-P:** Limits which tokens are even available

```
Both control randomness, but differently:

Temperature=0, Top-P=1.0:
→ Always deterministic (high temp conditioning is ignored if only 1 option)

Temperature=1.0, Top-P=0.5:
→ Random, but only from the top 50% of tokens

Temperature=1.0, Top-P=1.0:
→ Normal randomness
```

### When to Use

```
top_p=0.5:   Very focused, rare outputs excluded
top_p=0.9:   Balanced (often used with temperature)
top_p=1.0:   Include all possibilities (default)
```

**Combined use:**
```
For creative writing:
- temperature=1.0, top_p=0.9 (slightly random, no garbage)

For factual answers:
- temperature=0.5, top_p=1.0 (mostly deterministic, any token possible if needed)

For code:
- temperature=0.3, top_p=1.0 (mostly deterministic, working code)
```

---

## Other Important Parameters

### Frequency Penalty
Reduces repetition by penalizing tokens that already appeared.

```
Default: 0 (no penalty)
Range: -2 to 2

Positive value: Penalizes repeated words
Negative value: Encourages repeated words (rare)

Example:
Prompt: "List 5 ideas"
Without penalty: "Ideas are... ideas about... ideas for..."
With penalty=0.5: "Ideas are... suggestions for... approaches to..."
(Avoids repeating "ideas")
```

### Presence Penalty
Reduces repetition of topics by penalizing similar concepts.

```
Similar to frequency_penalty but applies to semantically similar tokens, not just identical ones.
```

### Top-K
**What it is:** Only consider the K most likely tokens.

```
top_k=10: Only pick from the top 10 most probable tokens
top_k=50: Only pick from the top 50 most probable tokens

Similar to top_p, but absolute count instead of cumulative probability
```

---

## Common Parameter Combinations

### For Factual Questions
```python
max_tokens=1000
temperature=0.2        # Very consistent
top_p=1.0
frequency_penalty=0
```

Result: Reliable, accurate, consistent answers

### For Creative Writing
```python
max_tokens=2000
temperature=1.2        # Creative
top_p=0.9             # Focused variety
frequency_penalty=0.5 # Avoid repetition
```

Result: Diverse, creative, interesting responses

### For Code Generation
```python
max_tokens=1500
temperature=0.2        # Consistent (working code)
top_p=1.0
frequency_penalty=0
```

Result: Working, clean code

### For Brainstorming
```python
max_tokens=500
temperature=1.0        # Balanced creativity
top_p=0.9             # Good variety
frequency_penalty=0.6 # Avoid same idea twice
```

Result: Multiple diverse ideas

### For Customer Service Bot
```python
max_tokens=250
temperature=0.5        # Slightly conversational
top_p=1.0
frequency_penalty=0.3 # Professional, not robotic
```

Result: Helpful, natural-sounding responses

---

## Important Notes

### Parameters Vary by Provider
OpenAI, Anthropic, Google each have slightly different parameter sets:

```
OpenAI: temperature, top_p, top_k, frequency_penalty, presence_penalty
Anthropic (Claude): temperature, top_p, top_k
Google (Gemini): temperature, top_p, top_k, max_output_tokens
```

Check your provider's documentation.

### Parameter Interactions
Temperature and top_p interact:

```
High temperature + low top_p = Strange (extreme randomness, but limited options)
Low temperature + high top_p = Efficient (deterministic, any token allowed but not used)

Use together meaningfully, or just use one.
```

### Testing is Key
Different applications need different parameters. Test and tune:

```
Start with defaults
Run several times
Adjust parameters
Test again
Find what works for your use case
```

---

## Self-Check

Can you answer:

- [ ] "What does temperature=0 do?" (Always pick highest probability token - deterministic)
- [ ] "Why would you use max_tokens=100?" (Short, cheap answers)
- [ ] "What's the difference between top_p and top_k?" (Top_p: cumulative probability; top_k: top count)
- [ ] "Which parameter do you adjust for longer responses?" (max_tokens)
- [ ] "What parameter reduces repeated words?" (frequency_penalty)

Ready for **[TIER-1-04-Prompt-Engineering-Fundamentals.md](TIER-1-04-Prompt-Engineering-Fundamentals.md)** →

Next: How to write prompts that get better results from LLMs.
