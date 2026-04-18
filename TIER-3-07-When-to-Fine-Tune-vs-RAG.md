# TIER 3-07: When to Fine-Tune vs RAG
## Making the Right Architectural Choice

---

## The Decision Matrix

```
Question: Should I fine-tune or use RAG?

Answer depends on:
1. How often does your knowledge update?
2. How specific is your domain knowledge?
3. What's your budget?
4. How much data do you have?
5. How fast do you need results?
```

---

## RAG: Best For

### When RAG is the Right Choice
```
✅ Knowledge changes frequently
✅ Need current information
✅ Have less than 10K training examples
✅ Want to keep secrets (don't share training data)
✅ Need quick deployment (hours, not days)
✅ Have budget limitations
✅ Multiple domains to support
```

### RAG Examples
```
- Company knowledge base (policies change monthly)
- FAQ system (new questions added weekly)
- Customer support (dynamic docs)
- News summarization (current events)
- Real-time Q&A over documents
```

### RAG Workflow
```
1. Load documents
2. Create embeddings (once)
3. Store in vector DB (once)
4. For each query:
   - Retrieve relevant docs
   - Send to LLM with context
   - Get answer

Timeline: Hours to deploy
Cost: Low ongoing (just API calls)
Maintenance: Add docs as needed
```

---

## Fine-Tuning: Best For

### When Fine-Tuning is the Right Choice
```
✅ Knowledge is stable/not changing
✅ Need specialized behavior (style, format, reasoning)
✅ Have 1K+ training examples
✅ Want faster inference (no retrieval needed)
✅ Have consistent performance requirements
✅ Domain very specific (medical, legal)
✅ Can afford retraining
```

### Fine-Tuning Examples
```
- Legal document classification (stable taxonomy)
- Medical diagnostic support (established knowledge)
- Content moderation (consistent policy)
- Brand voice matching (specific tone)
- Specialized reasoning (financial analysis)
```

### Fine-Tuning Workflow
```
1. Prepare 1000+ training examples
2. Format and validate data
3. Fine-tune model (24-48 hours)
4. Evaluate on test set
5. Deploy fine-tuned model
6. Monitor performance

Timeline: 1-2 weeks
Cost: Training + higher per-token rates
Maintenance: Retrain when data changes
```

---

## Head-to-Head Comparison

| Factor | RAG | Fine-Tuning |
|--------|-----|-------------|
| **Setup Time** | Hours | Days-Weeks |
| **Data Required** | 100-1000 docs | 1000+ examples |
| **Cost to Train** | $0 | $100-10,000 |
| **Update Frequency** | Real-time | Monthly |
| **Knowledge Cutoff** | None (always current) | Needs retraining |
| **Inference Speed** | Slower (retrieval) | Faster (no retrieval) |
| **Inference Cost** | Lower | Higher |
| **Quality Control** | Easy (change docs) | Hard (retrain needed) |
| **Best For** | Frequently changing | Stable knowledge |

---

## Decision Tree

```
Start: Should I fine-tune or use RAG?

1. Does knowledge change monthly+?
   → YES: Use RAG
   → NO: Continue

2. Do you have 1000+ training examples?
   → YES: Continue
   → NO: Use RAG

3. Is inference speed critical?
   → YES: Fine-tune
   → NO: Continue

4. Do you need specialized behavior/style?
   → YES: Fine-tune
   → NO: Use RAG

Result: Fine-tune if yes to #3 or #4, else RAG
```

---

## Hybrid Approach (Best of Both)

### Scenario
```
You have:
- Legal documents (stable, use fine-tuning for behavior)
- Current case law (changing, use RAG)
```

### Solution
```
1. Fine-tune model on legal writing style
2. Use RAG for current case law docs
3. Combine: Fine-tuned model + RAG retrieval

Result: Specialized model with current knowledge
```

### Code
```python
# Use fine-tuned model
fine_tuned_llm = ChatOpenAI(model="ft:gpt-3.5-turbo-...")

# Add RAG on top
qa = RetrievalQA.from_chain_type(
    llm=fine_tuned_llm,  # Fine-tuned
    chain_type="stuff",
    retriever=law_docs_retriever  # Current docs
)

# Query uses both
answer = qa.invoke("Interpret this case...")
```

---

## Real Scenarios

### Scenario 1: Customer Support Bot

**Situation:**
- Policies change weekly
- 500 help articles
- Need current info
- Budget: Limited

**Decision:** ✅ RAG
- Query over help articles
- Retrieval finds relevant docs
- LLM generates answer
- Updates: Just upload new docs

### Scenario 2: Medical Diagnosis Support

**Situation:**
- Knowledge base stable (medical facts don't change)
- 5000+ training examples (medical database)
- Need consistent diagnosis format
- Domain specialized

**Decision:** ✅ Fine-tune
- Train on medical examples
- Fine-tuned model = consistent medical reasoning
- Fast inference
- Quarterly retraining if new protocols added

### Scenario 3: Company Knowledge Base

**Situation:**
- Policies, procedures, org structure
- Changes: Monthly
- 100 documents
- Multiple teams

**Decision:** ✅ RAG
- Upload all docs
- Employees query
- Get up-to-date answers
- Add new docs as created

### Scenario 4: Patent Classification

**Situation:**
- 10K patents classified by category
- Categories stable
- Accurate classification needed
- Speed important

**Decision:** ✅ Fine-tune
- Train on patent corpus
- Fine-tuned model learns to classify
- Fast inference
- Retrain annually

---

## Cost Analysis

### RAG Costs
```
Setup: $0
Ongoing/month:
- 10K queries
- 500 tokens per query
- $0.03 per 1K tokens (chat)

Cost: (10K × 500) / 1000 × $0.03 = $150/month

Over 1 year: $1,800
```

### Fine-Tuning Costs
```
Setup:
- Training: $100-500 (depends on data size)
- Infrastructure: $0 (API handles it)

Ongoing/month:
- 10K queries
- 500 tokens per query
- $0.06 per 1K tokens (fine-tuned, ~2x cost)

Cost: (10K × 500) / 1000 × $0.06 = $300/month

Over 1 year: $300 (setup) + $3,600 = $3,900
```

### Decision
```
If knowledge changes frequently: RAG ($1,800/year)
If knowledge stable 2+ years: Fine-tuning ($3,900/year + retraining)
```

---

## Hybrid Cost

```
1. Fine-tune model: $300
2. RAG setup: $0
3. Ongoing:
   - Fine-tuned model: $300/month (higher rate)
   - RAG retrieval: ~$50/month (cheap)
   
Total: $350/month + $300 setup

When it's worth it:
- You need specialized behavior + current knowledge
- Cost premium < value delivered
- Medical/legal/domain-specific with updates
```

---

## Migration Path

### Start with RAG, Upgrade to Fine-Tuning

```
Month 1: Deploy RAG
- Load documents
- Query them
- Collect queries and answers

Month 2-3: Analyze
- Which queries need specialized behavior?
- Is performance consistent?
- Do patterns emerge?

Month 4: Fine-tune
- If patterns found: Create training dataset
- Fine-tune model
- Replace RAG LLM with fine-tuned

Result: Optimized system
```

---

## Self-Check

Can you answer:

- [ ] "When should you use RAG?" (When knowledge changes frequently)
- [ ] "When should you use fine-tuning?" (When knowledge is stable + domain specific)
- [ ] "What's the hybrid approach?" (Fine-tune for behavior, RAG for current data)
- [ ] "How does cost compare?" (Fine-tuning more expensive but often worth it)
- [ ] "How to decide?" (Use the decision tree)

---

## Congratulations! 🎉

**You've completed the full GenAI curriculum!**

### TIER 0: Foundations ✅
- What is AI, ML, DL
- Neural Networks
- Transformers
- Tokens

### TIER 1: LLMs ✅
- How LLMs work
- Parameters and prompting
- Limitations

### TIER 2: Building ✅
- LangChain
- Chains and templates
- Embeddings and RAG
- Build a working app

### TIER 3: Advanced ✅
- Advanced RAG
- Tools and agents
- LangGraph workflows
- Production deployment
- Cost optimization
- Architectural decisions

---

## Your Next Steps

1. **Choose a project** from the ideas below
2. **Build something** with TIER 2-3 knowledge
3. **Deploy it** to production
4. **Monitor it** for quality/costs
5. **Iterate** based on real usage

### Project Ideas
- Customer support chatbot (RAG + agents)
- Document analyzer (advanced RAG)
- Internal knowledge base (RAG)
- Automated research tool (agents + RAG)
- Code reviewer (fine-tuned + tools)

---

## Keep Learning

This handbook covers:
- ✅ GenAI fundamentals
- ✅ LLM usage
- ✅ RAG systems
- ✅ Agents and workflows
- ✅ Production deployment

Still to explore:
- Multimodal models (images + text)
- Video generation
- 3D generation
- Robotics
- Specialized domains

**Never stop learning.** The field evolves weekly. Subscribe to:
- LangChain docs
- OpenAI/Anthropic updates
- ArXiv ML papers
- Community forums

---

**You're ready to build production GenAI systems.** 🚀

Good luck!
