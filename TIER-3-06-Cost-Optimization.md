# TIER 3-06: Cost Optimization
## Reducing LLM API Costs

---

## The Cost Problem

```
Using GPT-4 for everything:
- $0.03 per 1K input tokens
- $0.06 per 1K output tokens

1 million queries:
- 1000 tokens per query = 1B tokens
- Cost: $30,000+ per month

Using GPT-3.5 for most tasks:
- $0.50 per 1M tokens
- Same queries: ~$500/month
```

**70x cost reduction by choosing right model!**

---

## Strategy 1: Model Selection

### Chart: Speed vs Quality vs Cost
```
Fast & Cheap ← GPT-3.5 Turbo, Claude Haiku
Balanced ← Claude Sonnet, GPT-4 Turbo
Expensive & Best ← GPT-4, Claude Opus

Rule of thumb:
- Customer-facing: Use best (GPT-4/Claude Opus)
- Internal analysis: Use cheap (GPT-3.5/Haiku)
- General tasks: Use middle (Sonnet/Turbo)
```

### Routing by Task
```python
def get_llm_for_task(task_type):
    if task_type == "customer_response":
        return ChatOpenAI(model="gpt-4")  # Best quality
    elif task_type == "classification":
        return ChatOpenAI(model="gpt-3.5-turbo")  # Fast, cheap
    else:
        return ChatAnthropic(model="claude-3-sonnet")  # Balanced

llm = get_llm_for_task(task_type)
result = llm.invoke(prompt)
```

---

## Strategy 2: Reduce Token Usage

### Shorter Prompts
```
❌ Long: "You are an expert... with 20 years... Please analyze..."
✅ Short: "Analyze: {text}"

Cost reduction: ~20%
```

### Few-Shot Examples (Carefully)
```
❌ Many examples: 10 examples × 100 tokens = 1000 token overhead
✅ Few examples: 2 examples × 100 tokens = 200 token overhead

Cost reduction: ~80%
```

### Summary Before Processing
```
❌ Send whole 50-page document: 10,000 tokens
✅ Send 1-page summary: 500 tokens, then ask question

Cost reduction: ~95%
```

---

## Strategy 3: Caching

### Response Caching
```python
from functools import lru_cache
import json

# Cache responses
@lru_cache(maxsize=10000)
def get_response(prompt_hash):
    result = llm.invoke(prompt)
    return result

# For repeated queries
get_response(hash(prompt))  # Returns cached result (instant, free)
```

### Prompt Caching (OpenAI)
```python
# Cache system prompt + context
messages = [
    {
        "type": "text",
        "text": "You are a helpful...",  # This gets cached
        "cache_control": {"type": "ephemeral"}
    },
    {"type": "text", "text": "Question: ..."}
]

response = client.messages.create(
    model="gpt-4-turbo",
    system=messages  # Cached tokens cost 90% less!
)
```

**Savings:** 90% on repeated cached tokens.

---

## Strategy 4: Batch Processing

### API Batch Jobs (Cheaper)
```python
# Regular API (real-time)
for query in queries:
    result = llm.invoke(query)
    
# Cost: Normal rate ($0.03 per 1K tokens)

# Batch API (overnight)
batch_results = batch_api.submit_batch(queries)

# Cost: 50% discount!
# Result ready next morning
```

**Savings:** 50% if you can wait.

---

## Strategy 5: Smarter Retrieval

### Fewer Documents Retrieved
```
❌ k=20: Retrieve 20 documents, process all
✅ k=5: Retrieve 5, usually sufficient

Cost in context: 4x reduction
```

### Query Compression
```python
# Compress query first
original = "Long question that could be shorter?"
compressed = "Short version?"

# Results still good, fewer tokens
result = llm.invoke(compressed)

Savings: ~50% on prompt tokens
```

---

## Strategy 6: Stratified Routing

```python
def smart_routing(task):
    # Simple tasks: cheap model
    if task.complexity == "low":
        return ChatOpenAI(model="gpt-3.5-turbo")
    
    # Medium tasks: middle model
    elif task.complexity == "medium":
        return ChatAnthropic(model="claude-3-sonnet")
    
    # Complex tasks: best model
    else:
        return ChatOpenAI(model="gpt-4")

# Average cost per request drops significantly
```

---

## Strategy 7: Summarization Pipeline

```
Large document (50 pages)
    ↓
Summarize to 1 page (1000 tokens)
    ↓
Question about summary (not full doc)
    ↓
30x token reduction!
```

```python
from langchain.chains.summarize import load_summarize_chain

# Summarize first
summary_chain = load_summarize_chain(llm, chain_type="map_reduce")
summary = summary_chain.run(large_document)

# Then ask question about summary
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=summarizer_retriever
)
```

---

## Real Math: Optimization Impact

### Before Optimization
```
- 1 million queries/month
- 1000 tokens per query (average)
- GPT-4 for everything
- Total: 1B tokens × $0.03 = $30,000/month
```

### After Optimization
```
- 70% of queries with GPT-3.5: 700K queries
  Cost: 700M tokens × $0.0005 = $350

- 20% with Claude Sonnet: 200K queries
  Cost: 200M tokens × $0.0015 = $300

- 10% with GPT-4: 100K queries
  Cost: 100M tokens × $0.03 = $3,000

- Caching saves 20%: -$760

- Total: $2,890/month (90% reduction!)
```

---

## Monitoring Costs

```python
from datetime import datetime

class CostTracker:
    def __init__(self):
        self.costs = []
    
    def log_request(self, model, input_tokens, output_tokens):
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        self.costs.append({
            "timestamp": datetime.now(),
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost
        })
    
    def get_monthly_cost(self):
        return sum(c["cost"] for c in self.costs)
    
    def get_cost_by_model(self):
        by_model = {}
        for c in self.costs:
            by_model.setdefault(c["model"], 0)
            by_model[c["model"]] += c["cost"]
        return by_model

tracker = CostTracker()

# Track every request
tracker.log_request("gpt-4", 500, 100)
tracker.log_request("gpt-3.5-turbo", 300, 50)

print(f"Monthly cost: ${tracker.get_monthly_cost():.2f}")
print(f"By model: {tracker.get_cost_by_model()}")
```

---

## Cost vs Quality Tradeoff

| Strategy | Cost Savings | Quality Impact | When to Use |
|----------|---|---|---|
| Cheap models | 90% | Medium | Background tasks |
| Shorter prompts | 20% | Low | All |
| Caching | 80-90% | None | Repeated queries |
| Batch processing | 50% | None | Non-urgent |
| Fewer documents | 60% | Medium | When possible |
| Summarization | 80% | Low | Large docs |
| Routing | 70% | Low | Mixed complexity |

---

## Self-Check

Can you:

- [ ] Choose the right model for a task?
- [ ] Write concise prompts?
- [ ] Implement caching?
- [ ] Set up cost tracking?
- [ ] Calculate savings?

Ready for **[TIER-3-07-When-to-Fine-Tune-vs-RAG.md](TIER-3-07-When-to-Fine-Tune-vs-RAG.md)** →

Next: Make architectural decisions.
