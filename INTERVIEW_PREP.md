# GenAI Interview Prep - Real Questions & Answers

---

## TIER 0-1 Level Questions

### 1. Explain the difference between AI, Machine Learning, and Deep Learning.

**Answer:**
- **AI**: Broad field - any technique that makes computers act intelligently
- **ML**: Subset of AI - computers learn patterns from data (decision trees, random forests, neural nets)
- **DL**: Subset of ML - uses neural networks with multiple layers to learn complex patterns

**Example:** Spam detection is ML. ChatGPT is DL.

---

### 2. What is a Transformer and why is it important?

**Answer:**
A Transformer is an architecture that processes sequences of data using **attention mechanisms**. Instead of processing words one at a time, it looks at all words simultaneously and learns which ones matter for each task.

**Why important:** Enables parallelization (faster training), handles long-range dependencies better, foundation for modern LLMs (GPT, Claude, etc.).

---

### 3. What are tokens and why do we count them?

**Answer:**
Tokens are chunks of text. "Hello world" = 2 tokens. "LLMs" = 1 token.

**Why count:**
- API charges per token (not per word)
- Context window limit (e.g., GPT-4 has 8K/128K token limit)
- Affects cost and speed

---

### 4. What is an embedding?

**Answer:**
An embedding converts text into a vector of numbers that represents meaning.

Example:
- "cat" → [0.2, -0.5, 0.8, ...]
- "dog" → [0.3, -0.4, 0.7, ...]
- "car" → [0.9, 0.1, -0.2, ...]

Similar words have similar vectors. Used for semantic search.

---

### 5. How does an LLM generate text?

**Answer:**
Step-by-step process:
1. Convert prompt to tokens
2. Pass through neural network layers
3. Network predicts probability of next token
4. Sample based on probability (or pick highest)
5. Add new token to prompt
6. Repeat until stop token or max length reached

That's why text appears word-by-word in ChatGPT.

---

### 6. What is temperature and how does it affect output?

**Answer:**
Temperature controls randomness in predictions (0-2 scale typically).

- **Temperature = 0**: Always pick highest probability token (deterministic, boring)
- **Temperature = 1**: Normal randomness
- **Temperature > 1**: More random, creative (risky for factual tasks)

**Use case:**
- Factual Q&A: temp = 0
- Creative writing: temp = 0.7-1.0

---

### 7. What is hallucination in LLMs?

**Answer:**
LLM confidently generates false information that sounds plausible.

**Why it happens:**
- No access to real-time data
- Trained to predict next token, not verify truth
- Doesn't know what it doesn't know

**Example:**
"Who was the CEO of Tesla in 2025?" → May fabricate a name if not in training data

**Solutions:**
- RAG (give it real documents to reference)
- Fact-checking layer
- Acknowledge uncertainty in prompt

---

### 8. What's the difference between base models and chat models?

**Answer:**
- **Base model**: Raw language model. Completes text but not good at instructions.
  - Prompt: "Q: What is AI?"
  - Output: "A: AI is artificial intelligence which..."

- **Chat model**: Fine-tuned for instruction following and dialogue.
  - Prompt: "What is AI?"
  - Output: "AI stands for Artificial Intelligence..."

**Use base for:** Text generation, creative writing  
**Use chat for:** Q&A, instructions, conversations

---

### 9. What is RLHF and why does it matter?

**Answer:**
RLHF = Reinforcement Learning from Human Feedback

Process:
1. Train base model on text data
2. Have humans rate model outputs (good vs bad)
3. Use ratings to fine-tune model
4. Model learns to generate outputs humans prefer

**Why it matters:** Makes models safer, more helpful, more aligned with human preferences.

---

### 10. Explain attention mechanism briefly.

**Answer:**
Attention lets the model decide which parts of input are important for each output token.

Example: "The bank is by the river"
- When predicting next word after "bank", model pays attention to "river" and "by"
- Understands "bank" = geography, not finance

**Multi-head attention:** Multiple attention mechanisms in parallel, each learning different relationships.

---

## TIER 2 Level Questions

### 11. What is RAG and when would you use it instead of fine-tuning?

**Answer:**
RAG = Retrieval-Augmented Generation

Process:
1. User asks question
2. Retrieve relevant documents from database
3. Pass documents + question to LLM
4. LLM answers based on documents

**When to use RAG:**
- Knowledge changes frequently (e.g., company policies)
- Don't want to retrain model (cheaper)
- Need current information (news, real-time data)
- Have less than 10K training examples

**When to use fine-tuning:**
- Knowledge is stable
- Need specialized behavior/style
- Have 1000+ training examples
- Speed is critical

---

### 12. What's the difference between embedding and RAG?

**Answer:**
- **Embedding**: Converts text to vector (meaning representation)
- **RAG**: Uses embeddings to retrieve relevant documents, then sends them to LLM

RAG = Embeddings + Document Retrieval + LLM

---

### 13. How does semantic search work?

**Answer:**
1. Create embeddings for all documents (once)
2. Create embedding for query
3. Find documents with embeddings closest to query (using cosine similarity)
4. Return most similar documents

**Why it works:** Semantically similar texts have similar embeddings.

Example:
- Query: "How do I make coffee?"
- Document: "Brewing instructions for espresso"
- These are semantically similar even with different words

---

### 14. What is LangChain and what problems does it solve?

**Answer:**
LangChain is a framework for building LLM applications.

**Problems it solves:**
- Boilerplate: Handling prompts, API calls, errors
- Chaining: Connect multiple LLMs/tools together
- Memory: Keep conversation history
- Retrieval: Connect to documents/databases
- Tools: Call external functions (calculators, APIs)

**Example without LangChain:**
```
Manual API calls, error handling, prompt formatting
= 50+ lines of code
```

**With LangChain:**
```
qa = RetrievalQA.from_chain_type(llm, retriever)
answer = qa.invoke("question")
= 3 lines
```

---

### 15. Explain vector databases and why they're needed.

**Answer:**
Vector databases store embeddings and allow fast similarity search.

**Why needed:**
- Regular databases can't efficiently search by meaning
- Embeddings are high-dimensional (300-3000 dimensions)
- Need special indexing for fast nearest-neighbor search

**Examples:** Pinecone, Weaviate, Chroma, Milvus

**Use case:** Search 1M documents for "How do I reset password?" in milliseconds

---

## TIER 3 Level Questions

### 16. Design a production GenAI system. What would you consider?

**Answer:**
Key considerations:

1. **Data Pipeline**
   - How often does data change?
   - How much data?
   - Quality/cleaning needed?

2. **Model Selection**
   - Speed vs quality tradeoff
   - Cost per request
   - Use cheap model for simple tasks, expensive for complex

3. **Architecture**
   - RAG or fine-tuning?
   - Agent or simple chain?
   - Need tools/function calling?

4. **Infrastructure**
   - API or self-hosted?
   - Scaling needs?
   - Latency requirements?

5. **Monitoring**
   - Track accuracy/quality
   - Monitor costs
   - Watch for hallucinations
   - Response time alerts

6. **Fallbacks**
   - What if API fails?
   - Retry logic with backoff
   - Cache responses

---

### 17. When would you use agents vs. simple chains?

**Answer:**
**Simple Chain:**
- Fixed sequence of steps
- Predictable inputs/outputs
- Low complexity

Example: Summarize → Translate

**Agents:**
- Variable number of steps
- Decide at runtime what to do
- Can use tools/functions

Example: "Answer any question using available tools"

**When to use agents:**
- Unclear path to solution
- Need tool selection
- Complex multi-step reasoning
- User can ask many types of questions

---

### 18. What's the difference between LangChain and LangGraph?

**Answer:**
- **LangChain**: Build chains and basic workflows
- **LangGraph**: Build stateful, complex workflows with cycles and conditions

**LangGraph example:**
```
Decide type of query
→ Route to different chain
→ If uncertain, ask human
→ Loop back based on response
```

**When to use LangGraph:**
- Need complex state management
- Loops and cycles
- Human-in-the-loop decisions
- Production systems with error recovery

---

### 19. How would you optimize costs for an LLM application?

**Answer:**
7 strategies:

1. **Model Selection**: Use cheap model (GPT-3.5) for 70% of tasks, expensive (GPT-4) for 30%
2. **Shorter Prompts**: Remove unnecessary words (saves 20%)
3. **Caching**: Cache repeated prompts (saves 90% on cached tokens)
4. **Batch Processing**: Use batch API overnight (50% discount)
5. **Fewer Documents**: Retrieve only 5 docs instead of 20
6. **Query Compression**: Shorten user query before sending
7. **Summarization**: Summarize large docs before asking questions

**Real example:** 90% cost reduction without quality loss

---

### 20. What are the tradeoffs between different RAG approaches?

**Answer:**

| Approach | Speed | Quality | Complexity |
|----------|-------|---------|-----------|
| Stuff (simple) | Fast | Medium | Low |
| Map-Reduce | Slower | High | Medium |
| Refine | Slowest | Highest | High |
| Hierarchical | Fast | High | High |
| Multi-query | Medium | Highest | Medium |

**Stuff:** Send all docs at once (simple, works for <20 docs)

**Map-Reduce:** Process each doc separately, combine answers (good for many docs)

**Hierarchical:** Build tree of documents, retrieve smartly (good for large corpus)

**Multi-query:** Ask question in multiple ways, get diverse results (best quality)

---

## How to Prepare

### Before Interview
1. Read TIER 0-1 thoroughly
2. Do 5-10 mock projects (RAG app, prompt engineering)
3. Practice explaining concepts simply
4. Know the GLOSSARY cold

### During Interview
- Ask clarifying questions
- Think out loud
- Admit what you don't know
- Give practical examples
- Show you understand tradeoffs

### Common Mistakes to Avoid
- Overcomplicating solutions
- Not mentioning monitoring/costs
- Assuming LLMs are always accurate
- Not asking clarifying questions
- Technical jargon without explanation

---

## Self-Check Before Interview

Can you explain:
- [ ] How LLMs generate text (step by step)
- [ ] What RAG is and when to use it
- [ ] Temperature, top-p, and how they affect output
- [ ] Embeddings and semantic search
- [ ] The difference between base models and chat models
- [ ] Why hallucinations happen
- [ ] When to fine-tune vs RAG
- [ ] How to reduce LLM costs
- [ ] What a vector database is
- [ ] How to design a production system

If you can answer 8/10, you're interview-ready.

---

Good luck! 🚀
