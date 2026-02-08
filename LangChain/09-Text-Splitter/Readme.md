# Text Splitters

## What is Text Splitting?

Text splitting is the process of partitioning large documents into smaller, semantically coherent chunks before processing. This is necessary because LLMs have finite context windows, embeddings perform poorly on very long texts, and RAG systems require focused, relevant chunks for retrieval accuracy.

---

## 2️⃣ Why Text Splitters Are Mandatory in GenAI Systems

### Problem Without Splitting

* Token limit exceeded ❌
* Poor embeddings ❌
* Wrong search results ❌
* Hallucinations ❌
* High cost ❌

### What Splitting Fixes

| Area          | Benefit                 |
| ------------- | ----------------------- |
| Embeddings    | Better semantic meaning |
| Search (RAG)  | Precise retrieval       |
| Summarization | Less hallucination      |
| Cost          | Lower API usage         |
| Performance   | Faster indexing         |

👉 **No production RAG system works without text splitters.**

---

## 3️⃣ Core Parameters (Very Important)

Before learning types, understand **these 3 knobs**:

### 🔹 Chunk Size

* Size of each chunk (characters / tokens)
* Typical range: **300–800 characters**

### 🔹 Chunk Overlap

* Repeats some content between chunks
* Prevents context loss at boundaries

👉 Rule of Thumb:

```
overlap = 10–20% of chunk_size
```

### 🔹 Separators

* Where text is allowed to break
* Example: `\n\n`, `.`, ` `

---

## 4️⃣ Types of Text Splitters in LangChain

LangChain provides **multiple splitter strategies** because **one size never fits all**.

---

## 5️⃣ Length-Based Text Splitter (Beginner Level)

### 🔹 What It Does

Splits text **purely by length**, ignoring meaning.

### 🔹 When to Use

* Logs
* Raw scraped data
* Very fast pipelines

### ❌ Problems

* Cuts sentences in the middle
* Poor semantic chunks

### ✅ Example

```python
from langchain.text_splitter import CharacterTextSplitter

text = "Very large text content here..."

splitter = CharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_text(text)
```

🧠 **Tip:**
Use this **only when structure does not matter**.

---

## 6️⃣ Recursive Character Text Splitter (Industry Standard ⭐)

### 🔹 Why This Is the Most Important Splitter

This splitter tries **multiple levels** to split text **naturally**.

### 🔹 How It Works (Internally)

It attempts splitting in this order:

1. Paragraphs (`\n\n`)
2. Lines (`\n`)
3. Sentences (`.`)
4. Words (` `)
5. Characters (last fallback)

👉 It **respects language structure**, not just size.

---

### ✅ Best Use Cases

* PDFs
* Articles
* Blogs
* Research papers
* Docs

### ✅ Production-Ready Example

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", ".", " ", ""]
)

chunks = splitter.split_text(text)
```

🧠 **Tip:**

> If you remember only **one splitter**, remember **this one**.

---

## 7️⃣ Document-Based Splitters (Code, Markdown, HTML)

Some documents have **structure**, not plain text.

### 🔹 Why Normal Splitters Fail Here

* Code must stay together
* Markdown headings define meaning
* HTML tags indicate sections

---

### 🧩 Code Splitter (Example: Python)

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

python_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\nclass ", "\ndef ", "\n\n", "\n", " "]
)

chunks = python_splitter.split_text(python_code)
```

---

### 🧩 Markdown Splitter

```python
from langchain.text_splitter import MarkdownTextSplitter

splitter = MarkdownTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_text(markdown_text)
```

🧠 **Tip:**
Always **align splitter logic with document type**.

---

## 8️⃣ Semantic Text Splitting (Advanced / Experimental)

### 🔹 What It Tries to Do

Splits text based on **meaning change**, not size.

### 🔹 How It Works Conceptually

1. Split into sentences
2. Generate embeddings
3. Measure cosine similarity
4. Detect topic change
5. Split where meaning drops

---

### ❌ Why It’s Not Production-Ready Yet

* Expensive (many embeddings)
* Unstable thresholds
* Hard to tune
* Slow indexing

### ✅ When You Can Try It

* Research
* Mixed-topic documents
* Experiments

```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain.embeddings import OpenAIEmbeddings

splitter = SemanticChunker(
    OpenAIEmbeddings()
)

chunks = splitter.split_text(text)
```

🧠 **Advice:**

> Semantic splitting is **promising**, not **reliable** (yet).

---

## 9️⃣ Choosing the Right Splitter (Decision Table)

| Document Type | Recommended Splitter     |
| ------------- | ------------------------ |
| PDF / Blog    | RecursiveCharacter       |
| Plain logs    | Length-based             |
| Code          | Custom document splitter |
| Markdown      | MarkdownTextSplitter     |
| Mixed topics  | Semantic (experimental)  |

---

## 🔟 Best Practices (Real Industry Rules)

### ✅ Chunk Size

* Embeddings: **300–600**
* LLM context: **700–1000**

### ✅ Overlap

* 10–20%
* Avoid more → cost explosion

### ✅ Metadata

Always store:

* Source
* Page number
* Section

### ✅ Never

* Embed full documents
* Skip overlap
* Use semantic splitter blindly

---

## Where Text Splitter Fits in RAG Pipeline

```
Document Loader
      ↓
Text Splitter   ← (THIS STEP)
      ↓
Embeddings
      ↓
Vector Database
      ↓
Retriever
      ↓
LLM
```

---

## Production Considerations for Text Splitting

Optimize chunking strategy for your specific use case:

### Chunk Size Optimization
* Start with 500-character chunks and monitor retrieval quality
* Increase size for dense technical documents
* Decrease size for short documents or conversations
* Measure impact on embedding quality and retrieval accuracy

### Testing and Validation
* Test different overlap percentages (10-25%) for your content
* Monitor average chunk length to detect outliers
* Validate that important semantic boundaries aren't broken
* Measure retrieval precision before and after changes

### Performance Considerations
* Use streaming split for very large documents
* Consider semantic splitting for domain-specific content
* Cache splitting results to avoid reprocessing
* Monitor tokenization accuracy for your embedding model

### Quality Assurance
* Inspect random samples of chunks for coherence
* Verify that questions typically resolve within single chunks
* Monitor for orphaned or excessively short chunks
* Track splitting efficiency metrics

---

## Final Summary

* Text splitting is **mandatory**, not optional
* RecursiveCharacterTextSplitter is **default choice**
* Chunk overlap prevents context loss
* Code & markdown need **special handling**
* Semantic splitting is **experimental**
* Good splitting = better RAG accuracy

