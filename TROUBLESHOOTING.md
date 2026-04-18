# Troubleshooting Guide - Common Errors & Solutions

---

## API & Connection Errors

### Error: "Invalid API key" or "Authentication failed"

**Cause:** API key is wrong, expired, or not set correctly

**Solutions:**
- Use environment variables, not hardcoded keys
- Load from .env file using python-dotenv
- Check key is valid in provider's dashboard
- Verify environment variable name (OPENAI_API_KEY, etc.)

---

### Error: "Rate limit exceeded" or "Too many requests"

**Cause:** Making too many API calls too quickly

**Solutions:**
- Add delays between requests: `time.sleep(1)`
- Use batch API for non-urgent requests
- Implement caching for repeated queries
- Add exponential backoff for retries

---

### Error: "Connection timeout" or "Network error"

**Cause:** Network issues or API is slow/down

**Solutions:**
- Check internet connection
- Check provider's status page
- Increase timeout: `ChatOpenAI(request_timeout=60)`
- Try from different network

---

## LangChain Errors

### Error: "OutputParserException: Could not parse"

**Cause:** LLM output doesn't match expected format

**Solutions:**
- Use structured output parsers (JSON, CSV)
- Give format examples in prompt
- Test parser with sample outputs first
- Specify exact format: "Answer in JSON: {answer: '', confidence: 0-1}"

---

### Error: "No module named 'langchain_openai'"

**Cause:** LangChain package not installed or outdated

**Solutions:**
```
pip install langchain langchain-openai langchain-anthropic
pip install --upgrade langchain
```

---

### Error: "Retriever returned no documents"

**Cause:** Query doesn't match any documents in database

**Solutions:**
- Verify documents loaded: `print(len(docs))`
- Test retriever with known queries
- Check document chunking (not too small/large)
- Ensure embeddings created correctly

---

## Embedding & Vector Database Errors

### Error: "Embedding dimension mismatch"

**Cause:** Using different embedding models for storage and retrieval

**Solutions:**
- Use SAME embedding model for all documents
- Use SAME embedding model for queries
- Verify model: embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

---

### Error: "Vector store is empty"

**Cause:** Documents not added to vector store

**Solutions:**
```
documents = loader.load()
embeddings = OpenAIEmbeddings()
vector_store = Chroma.from_documents(documents, embeddings)
print(vector_store._collection.count())  # Should be > 0
```

---

## Hallucination & Quality Issues

### Problem: "LLM is making up facts"

**Solutions:**
1. Use RAG to provide real documents
2. Prompt engineering: "Say 'I don't know' if unsure"
3. Add fact-checking with second LLM
4. Set temperature=0 for factual tasks

---

### Problem: "Output is too short/too long"

**Solutions:**
- Use max_tokens: `ChatOpenAI(max_tokens=100)`
- Specify in prompt: "Answer in exactly 50 words"
- Use output parser to enforce format

---

## Performance Issues

### Problem: "Slow responses" or "High latency"

**Solutions:**
- Use cheaper/faster model: gpt-3.5-turbo vs gpt-4
- Implement caching for repeated queries
- Stream responses for immediate feedback
- Reduce retrieved documents: `search_kwargs={"k": 3}`
- Use async processing: `llm.ainvoke()`

---

## Cost Issues

### Problem: "High API costs"

**Solutions:**
- Use cheaper model (GPT-3.5 is 10x cheaper than GPT-4)
- Shorten prompts (remove unnecessary words)
- Implement caching (90% savings on repeated)
- Use batch API (50% cheaper, overnight)
- Monitor costs regularly

---

## Testing & Debugging

### General Debugging Tips

```
# 1. Add logging
import logging
logging.basicConfig(level=logging.DEBUG)

# 2. Test components individually
documents = retriever.get_relevant_documents(query)
response = llm.invoke(prompt)

# 3. Use assertions
assert len(documents) > 0, "Retriever failed"
assert len(response) > 0, "LLM failed"

# 4. Print intermediate states
print(f"Retrieved {len(docs)} docs")
print(f"Response length: {len(response)}")
```

---

## Quick Checklist When Something Breaks

- [ ] API key is valid?
- [ ] Internet connection working?
- [ ] All packages installed? `pip list`
- [ ] Packages updated? `pip install --upgrade`
- [ ] Correct import statements?
- [ ] Environment variables set?
- [ ] Tested components individually?
- [ ] Provider status page OK?
- [ ] Tried restart/reinstall?

---

## Getting Help

1. Read error message carefully - usually tells you the problem
2. Check LangChain documentation
3. Search for similar issues: GitHub, Stack Overflow
4. Provide context: code, full error, versions
5. Test each component in isolation

---

Good luck debugging! 🔧
