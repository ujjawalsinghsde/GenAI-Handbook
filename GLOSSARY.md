# 📖 GenAI Glossary
## Simple Explanations of All GenAI Terms

Whenever you see a term you don't understand, search here with **Ctrl+F**.

All terms organized alphabetically with simple explanations, real examples, and what interviewers want to hear.

---

## Language Model Concepts

### **Large Language Model (LLM)**
**Simple explanation:** A huge neural network trained on billions of words that can understand and generate text.

**Why "Large"?**
- Large dataset (billions of words)
- Large model (billions of parameters)

**Examples:** GPT-4, Claude 3, Llama 2, Gemini

**Interview answer:** "An LLM is a deep neural network trained on massive text data that learns linguistic patterns and can generate coherent text."

---

### **Token**
**Simple explanation:** A small piece of text. Usually a word, or a few characters.

**Real example:**
```
"Hello world" = 2 tokens (usually)
"Generative AI" = 2-3 tokens (depends on tokenizer)
"isn't" = 2 tokens (split into "is" and "n't")
```

**Why it matters:** LLMs charge per token. 1000 words ≈ 1300 tokens.

**Interview answer:** "Tokens are subword units. LLMs break text into tokens for processing. Tokenization affects cost and response length."

---

### **Transformer**
**Simple explanation:** A neural network architecture that's really good at understanding relationships between words in a sentence.

**Real-world analogy:**
Imagine reading a sentence: "The bank manager said the loan was approved."
- Your brain instantly understands "bank" means a financial institution (not river bank)
- Because "manager" and "loan" provide context
- Transformers do this using something called "attention" - they weigh which words matter most

**Key feature:** Can process all words in parallel (very fast)

**Interview answer:** "Transformers are neural architectures using self-attention mechanisms that can parallel process text and capture long-range dependencies."

---

### **Attention Mechanism**
**Simple explanation:** The ability to focus on the most important words when understanding text.

**Example:** In "The cat sat on the mat", when processing "cat", the attention mechanism:
1. Looks at all words: "The", "cat", "sat", "on", "the", "mat"
2. Realizes "sat" is more important than "the"
3. Focuses more on "sat" (the action)
4. Understands "cat" is the subject doing the action

**Interview answer:** "Attention mechanisms allow models to weight the importance of different input tokens when computing representations, enabling better context understanding."

---

### **Parameter**
**Simple explanation:** A weight or number in the neural network that the model learns during training.

**Analogy:** Like knobs you adjust on an amplifier. A LLM has billions of these knobs.

**Examples:**
- 7B parameters = 7 billion
- GPT-3 = 175B parameters
- More parameters usually = more powerful (but also slower & expensive)

**Interview answer:** "Parameters are learnable weights in a neural network adjusted during training to minimize loss."

---

### **Prompt**
**Simple explanation:** The instructions or question you give to an LLM.

**Examples:**
```
"What is the capital of France?" (simple prompt)
"Write a professional email asking for a deadline extension" (complex prompt)
"Translate this to Spanish and make it funny: [text]" (multi-step prompt)
```

**Interview answer:** "A prompt is the input text provided to an LLM that guides the model's generation of output."

---

### **Prompt Engineering**
**Simple explanation:** The art of writing prompts that get better results from LLMs.

**Good vs Bad Prompt:**

❌ **Bad:** "Tell me about Python"
✅ **Good:** "I'm a beginner programmer. Explain Python in 3 sentences with simple words, then give one beginner-friendly project idea."

**Techniques:**
- Be specific about what you want
- Give examples of good responses (few-shot)
- Break complex requests into steps
- Tell it to think step-by-step

**Interview answer:** "Prompt engineering is optimizing prompts to improve LLM output quality, relevance, and consistency."

---

### **Few-Shot Learning**
**Simple explanation:** Showing the LLM a few examples so it understands the pattern.

**Example:**
```
Few-shot prompt:
Translate English to French:
- Hello → Bonjour
- Good morning → Bon matin
- How are you? → Comment allez-vous?

Now translate: Good night → ?
```

**vs. Zero-shot:** Ask without examples (LLM already knows, so it tries anyway)

**Interview answer:** "Few-shot learning provides examples in the prompt to demonstrate the desired task before expecting the model to perform it."

---

### **Hallucination**
**Simple explanation:** When an LLM confidently makes up false information instead of saying "I don't know."

**Real example:**
```
Q: "What did CEO John Smith say about AI in 2023?"
A: "In his keynote, John Smith emphasized the importance of ethical AI..."
(But this speech never happened - the AI hallucinated it)
```

**Why it happens:** LLMs predict the next word based on probability. Sometimes they predict something that sounds plausible but is false.

**Interview answer:** "Hallucination occurs when an LLM generates confident but factually incorrect information. It happens because models predict likely text without access to real-time truth verification."

**How to prevent:** Use RAG, provide sources, ask it to cite information

---

### **Temperature**
**Simple explanation:** A setting that controls how creative vs. predictable the LLM's responses are.

**Scale:**
- Temperature = 0: Always pick the most likely word (deterministic)
- Temperature = 0.5: Somewhat predictable, some variety
- Temperature = 1: Balanced creativity and accuracy
- Temperature = 2: Very creative, might say weird things

**Use cases:**
- FAQ bot: Low temperature (0.2) - needs exact, consistent answers
- Brainstorming tool: High temperature (0.9) - needs creative ideas
- Chat: Medium temperature (0.7) - balanced

**Interview answer:** "Temperature controls randomness in text generation. Lower values produce deterministic outputs; higher values increase diversity."

---

### **Top-K and Top-P (Nucleus Sampling)**
**Simple explanation:** Ways to limit which words the model can pick next.

**Top-K:** "Pick from the top 40 most likely words"
**Top-P:** "Pick from words that make up the top 90% of probability"

**Interview answer:** "Top-K and Top-P are sampling strategies that limit vocabulary selection to improve output quality."

---

## Embedding & Semantic Search

### **Embedding**
**Simple explanation:** Converting text into a list of numbers that captures its meaning.

**How it works:**
- Word: "apple" → Numbers: [0.2, -0.5, 0.8, 0.1, ...]
- Words with similar meanings → Numbers far apart → close numerical values
- "apple" and "orange" have similar embeddings (both fruits)
- "apple" and "fork" have different embeddings

**Why it matters:**
- Lets computers understand meaning
- Makes semantic search possible
- Used in RAG systems

**Dimensions:** Embeddings have 768-4096 dimensions (like coordinates in multi-dimensional space)

**Interview answer:** "Embeddings are dense vector representations of text that capture semantic meaning, enabling semantic similarity calculations."

---

### **Vector Database**
**Simple explanation:** A special database that stores embeddings (number lists) and finds similar ones fast.

**Normal database:**
```
❌ Slow: "Find all documents about cats"
(Must read all text, compare keywords)
```

**Vector database:**
```
✅ Fast: Find similar embeddings to "cats"
(Just compare numbers, very fast)
```

**Examples:** Pinecone, Weaviate, Chroma, Faiss, OpenSearch

**Interview answer:** "Vector databases store embeddings for efficient similarity search using specialized indexing structures."

---

### **Semantic Search**
**Simple explanation:** Finding documents by meaning, not just keywords.

**Difference:**
- **Keyword search:** Find documents with word "river"
- **Semantic search:** Find documents about "flowing water"

**Interview answer:** "Semantic search finds relevant documents by comparing meaning (vector similarity) rather than text string matching."

---

## RAG & Knowledge Integration

### **Retrieval-Augmented Generation (RAG)**
**Simple explanation:** Giving an LLM documents to read before answering, so it has current knowledge.

**Problem it solves:**
- LLM trained in 2021, doesn't know current news
- LLM doesn't know your company's private documents

**How RAG works:**
1. User asks: "What's our newest product?"
2. System searches company docs for "newest product"
3. System finds: "Product X launched March 2024"
4. System gives this to LLM: "Answer using: [doc context]"
5. LLM answers using the recent info

**Interview answer:** "RAG combines document retrieval with LLM generation to provide grounded, up-to-date responses using external knowledge sources."

---

### **Context Window**
**Simple explanation:** The amount of text an LLM can read in one conversation.

**Examples:**
- Claude 3 Opus: 200K tokens ≈ 150,000 words
- GPT-4: 128K tokens ≈ 96,000 words
- Llama: 4K tokens ≈ 3,000 words

**Why it matters:** Larger window = can read more documents before answering

**Interview answer:** "Context window is the maximum number of input and output tokens an LLM can handle in a single request."

---

### **Document Chunking**
**Simple explanation:** Breaking large documents into smaller pieces so RAG works well.

**Why needed:**
- Document: 50,000 words (50 pages)
- Context window: 10,000 words max
- Solution: Split into chunks

**Example:**
```
Document: "The History of Rome (100 pages)"
Split into:
- Chunk 1: "Ancient Rome (30AD-100AD)"
- Chunk 2: "Imperial Rome (100AD-200AD)"
- Chunk 3: "Decline of Rome (300AD-476AD)"
```

**Interview answer:** "Document chunking divides text into manageable pieces (usually 256-1000 tokens) for efficient retrieval and processing in RAG systems."

---

### **Retriever**
**Simple explanation:** A system that finds relevant documents from a large collection quickly.

**Process:**
1. User asks something
2. Retriever converts it to embeddings
3. Searches vector database
4. Returns top 5 most similar documents

**Interview answer:** "A retriever is a component that searches a knowledge base and returns relevant documents based on semantic or keyword similarity."

---

## Tools & Frameworks

### **LangChain**
**Simple explanation:** A toolkit that makes building LLM applications easier (like a framework for web apps).

**What it does:**
- Connects to different LLMs
- Manages prompts and templates
- Chains operations together
- Handles document loading and splitting
- Manages memory and conversation

**Why use it:** Without LangChain, you write boilerplate code; with it, you focus on logic.

**Interview answer:** "LangChain is a Python/JavaScript framework providing modular abstractions for building LLM-powered applications with standardized interfaces."

---

### **Agent**
**Simple explanation:** An LLM that can use tools (functions) to take actions, not just answer questions.

**Simple Assistant:**
```
Q: "What's the weather?"
A: "I don't know" (it can't look up weather)
```

**Agent:**
```
Q: "What's the weather?"
Agent thinks: I should use the weather_api tool
Agent calls: weather_api(location="New York")
Agent gets: {temp: 72F, condition: "sunny"}
Agent answers: "It's 72F and sunny in New York"
```

**Interview answer:** "An agent is an LLM that can use tools/functions to perform actions and solve multi-step problems through reasoning loops."

---

### **Tool Calling (Function Calling)**
**Simple explanation:** Telling an LLM what tools it can use, and it decides when to use them.

**Tools example:**
- Calculator tool (for math)
- Web search tool (for current info)
- Email tool (to send messages)
- Database tool (to look up data)

**Interview answer:** "Tool calling enables LLMs to invoke external functions by generating structured outputs specifying which tool to use and with what parameters."

---

### **Chain**
**Simple explanation:** Connecting multiple steps together in sequence.

**Simple chain:**
```
Step 1: Take user question
Step 2: Search documents for relevant info
Step 3: Generate answer using found info
Step 4: Format and return answer
```

**Interview answer:** "A chain is a sequence of LLM calls and other logic combined to perform multi-step tasks where outputs of one step feed into the next."

---

## Optimization Concepts

### **Fine-Tuning**
**Simple explanation:** Retraining an LLM on your specific data to make it better for your use case.

**Example:**
- Base model: Knows general knowledge
- Fine-tune on: 1000 customer support examples
- Result: Model is excellent at customer support

**Interview answer:** "Fine-tuning adapts a pre-trained LLM to specific tasks by training it further on task-specific data, improving performance."

---

### **Quantization**
**Simple explanation:** Compressing a model to make it smaller and faster, with minimal quality loss.

**Example:**
- Original model: 32-bit numbers per parameter
- Quantized: 8-bit numbers per parameter
- Result: Model is 4x smaller, slightly slower, but still accurate

**Interview answer:** "Quantization reduces model size and inference latency by representing weights and activations with lower precision (e.g., 8-bit vs 32-bit)."

---

### **Caching**
**Simple explanation:** Saving LLM responses so you don't have to call it again for repeated questions.

**Example:**
```
Q1: "What is RAG?" → Call LLM → Save response
Q2: "What is RAG?" → Use saved response (instant!)
```

**Interview answer:** "Caching stores previously computed LLM outputs to reduce API calls and improve response latency for repeated queries."

---

### **Token Counting**
**Simple explanation:** Knowing how many tokens your prompt and response use (for cost estimation).

**Why:** You're charged per token (e.g., $0.01 per 1000 tokens)

**Estimate:** 1 word ≈ 1.3 tokens
- 1000 words ≈ 1300 tokens
- 100 pages ≈ 130,000 tokens

**Interview answer:** "Token counting measures input and output length to estimate API costs and ensure requests fit within context windows."

---

### **Batch Processing**
**Simple explanation:** Sending multiple requests together instead of one-at-a-time to save money.

**Example:**
- Send 100 requests one-by-one: Expensive
- Send 100 requests in a batch: 50% cheaper but slower

**Use case:** Night-time processing of many emails, documents, etc.

**Interview answer:** "Batch processing groups multiple API requests for more economical and efficient processing, trading latency for cost savings."

---

## Production Concepts

### **Hallucination Prevention**
**Simple explanation:** Techniques to stop LLMs from making up false information.

**Techniques:**
1. **RAG:** Give it real documents to cite
2. **Few-shot:** Show examples with citations
3. **Temperature:** Lower temperature = less creative = fewer hallucinations
4. **Validation:** Check if response matches source

**Interview answer:** "Prevention strategies include using RAG, few-shot examples, lower temperature, source verification, and explicit instructions to cite or avoid speculation."

---

### **Latency**
**Simple explanation:** How long it takes to get an answer (usually measured in seconds/milliseconds).

**Good latency:**
- Chat: <3 seconds
- Real-time: <500ms
- Batch: Can wait

**How to improve:**
- Use smaller models
- Use caching
- Use batch processing
- Quantization

**Interview answer:** "Latency is the time between sending a request and receiving a response. Lower latency is critical for real-time applications."

---

### **Throughput**
**Simple explanation:** How many requests you can handle per second.

**Example:**
- 10 requests/second good throughput
- 1000 requests/second excellent throughput

**How to improve:**
- More servers
- Batch processing
- Optimize model

**Interview answer:** "Throughput measures how many requests can be processed per unit time. Higher throughput enables serving more users simultaneously."

---

### **Cost Optimization**
**Simple explanation:** Making your LLM usage cheaper.

**Strategies:**
1. Use cheaper models for simple tasks
2. Reduce token usage (shorter prompts)
3. Use caching for repeated questions
4. Batch processing for bulk work
5. Fine-tune smaller models vs calling big ones

**Interview answer:** "Cost optimization involves selecting appropriate models, monitoring token usage, using caching, batching, and fine-tuning based on workload requirements."

---

### **Evaluation Metrics**
**Simple explanation:** How to measure if your LLM is actually good.

**Metrics:**
- **Accuracy:** Did it give the right answer?
- **Relevance:** Is the answer related to the question?
- **Coherence:** Is the answer clear and logical?
- **Factuality:** Are the facts correct?

**Interview answer:** "Evaluation metrics quantify LLM performance on specific dimensions like accuracy, relevance, and factuality to guide model selection and optimization."

---

## AWS-Specific Terms

### **Amazon Bedrock**
**Simple explanation:** AWS's managed service to use LLMs without running servers yourself.

**What it gives you:**
- Access to multiple LLMs (Claude, Llama, Mistral, etc.)
- No server management
- Pay per API call
- Easy to use from Lambda or other AWS services

**Interview answer:** "Amazon Bedrock is a fully managed service providing API access to multiple foundation models without infrastructure management."

---

### **Foundation Models**
**Simple explanation:** Large, pre-trained models that you can use or customize for your needs.

**Examples:**
- Claude (Anthropic/via Bedrock)
- GPT-4 (OpenAI)
- Llama (Meta)

**Interview answer:** "Foundation models are large pre-trained neural networks trained on broad data that serve as a starting point for various downstream tasks."

---

## Practice Questions

**Q1: A user asks your chatbot "What's the fastest car?" How might the model hallucinate?**
A: It might confidently state "The Bugatti Bolide is 500mph" (made up) instead of saying it's unsure or needs current data.

**Q2: Why is RAG better than just using an LLM?**
A: RAG gives the LLM real documents to cite, preventing hallucinations and ensuring current information.

**Q3: What's the difference between fine-tuning and RAG?**
A: RAG adds documents at query time (flexible). Fine-tuning retrains the model (permanent, best for specific tasks).

---

End of glossary. Use this when reading the modules!

