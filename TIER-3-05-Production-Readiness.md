# TIER 3-05: Production Readiness
## Deploying and Monitoring Systems

---

## Pre-Production Checklist

### Performance
- [ ] Response time < acceptable threshold
- [ ] Throughput meets requirements
- [ ] Latency is consistent

### Quality
- [ ] Test accuracy on real data
- [ ] Error rate < acceptable
- [ ] Hallucination rate measured

### Security
- [ ] API keys secured (.env, secrets manager)
- [ ] Input validation in place
- [ ] Rate limiting enabled
- [ ] No sensitive data in logs

### Scalability
- [ ] Can handle 10x traffic
- [ ] Database indexed
- [ ] Caching strategy implemented

---

## Logging

```python
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def process_query(query):
    logger.info(f"Processing query: {query[:50]}...")
    
    try:
        result = llm.invoke(query)
        logger.info(f"Success: {result[:50]}...")
        return result
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise
```

---

## Monitoring

### What to Monitor
```python
from prometheus_client import Counter, Histogram, Gauge

# Metrics
requests_total = Counter('requests_total', 'Total requests')
request_duration = Histogram('request_duration_seconds', 'Request duration')
active_requests = Gauge('active_requests', 'Active requests')
errors_total = Counter('errors_total', 'Total errors')

def process_with_metrics(query):
    requests_total.inc()
    active_requests.inc()
    
    start = time.time()
    try:
        result = llm.invoke(query)
        return result
    except Exception as e:
        errors_total.inc()
        raise
    finally:
        duration = time.time() - start
        request_duration.observe(duration)
        active_requests.dec()
```

---

## Error Handling

```python
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(
    wait=wait_exponential(multiplier=1, min=4, max=10),
    stop=stop_after_attempt(3)
)
def call_llm_with_retry(prompt):
    """Call LLM with automatic retry"""
    return llm.invoke(prompt)

# Use it
try:
    result = call_llm_with_retry(prompt)
except Exception as e:
    logger.error(f"Failed after retries: {e}")
    # Fallback or alert
```

---

## Rate Limiting

```python
from ratelimit import limits, sleep_and_retry
import time

@sleep_and_retry
@limits(calls=100, period=60)  # 100 calls per minute
def call_api(query):
    """Rate-limited API call"""
    return llm.invoke(query)
```

---

## Testing

### Unit Tests
```python
import pytest

def test_calculator_tool():
    assert calculator("2+2") == 4
    assert calculator("10*5") == 50

def test_retriever():
    docs = retriever.get_relevant_documents("test query")
    assert len(docs) > 0
```

### Integration Tests
```python
def test_full_pipeline():
    result = qa_chain.invoke("What is the return policy?")
    assert "policy" in result.lower()
    assert len(result) > 0
```

### Evaluation Metrics
```python
from langchain.evaluation import load_evaluator

evaluator = load_evaluator("qa")
result = evaluator.evaluate_strings(
    input="What is AI?",
    prediction="AI is...",
    reference="AI stands for..."
)
print(result["score"])  # Quality score
```

---

## Deployment Architectures

### Option 1: Simple API
```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/query")
async def query(question: str):
    result = qa_chain.invoke(question)
    return {"answer": result}

# Run: uvicorn app:app --reload
```

### Option 2: Docker
```dockerfile
FROM python:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0"]
```

### Option 3: Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm-app
  template:
    metadata:
      labels:
        app: llm-app
    spec:
      containers:
      - name: llm-app
        image: llm-app:latest
        ports:
        - containerPort: 8000
```

---

## Caching Strategy

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_cached_embedding(text):
    """Cache embeddings"""
    return embeddings.embed_query(text)

# Or with Redis
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def get_with_redis_cache(key):
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    
    result = expensive_operation()
    r.setex(key, 3600, json.dumps(result))  # Cache 1 hour
    return result
```

---

## Performance Optimization

### 1. Batch Processing
```python
# Process multiple queries efficiently
queries = ["What is AI?", "What is ML?", "What is DL?"]
results = llm.batch(queries)  # Faster than 3 separate calls
```

### 2. Streaming for Long Responses
```python
for chunk in llm.stream(prompt):
    print(chunk.content, end="", flush=True)  # User sees it immediately
```

### 3. Async Processing
```python
async def process_many(queries):
    tasks = [llm.ainvoke(q) for q in queries]
    results = await asyncio.gather(*tasks)
    return results
```

---

## Self-Check

Can you:

- [ ] Set up logging?
- [ ] Add monitoring/metrics?
- [ ] Implement retry logic?
- [ ] Write tests?
- [ ] Deploy with Docker?

Ready for **[TIER-3-06-Cost-Optimization.md](TIER-3-06-Cost-Optimization.md)** →

Next: Reduce costs while maintaining quality.
