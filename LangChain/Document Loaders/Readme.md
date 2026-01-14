# 📘 Document Loaders in LangChain

---

## 1️⃣ Why Document Loaders Exist (First Principles)

Large Language Models (LLMs):

* Do **not know your private data**
* Do **not know latest data**
* Cannot directly read **files, PDFs, databases, or websites**

👉 To solve this, we use **RAG (Retrieval-Augmented Generation)**.

### RAG High-Level Flow

```
External Data
   ↓
Document Loader   ← (THIS TOPIC)
   ↓
Text Splitter
   ↓
Embeddings
   ↓
Vector Database
   ↓
Retriever
   ↓
LLM Answer
```

**Document Loaders are the FIRST real-world bridge** between raw data and LLMs.

---

## 2️⃣ What is a Document Loader?

### Simple Definition

> A **Document Loader** loads data from any source and converts it into a **standard LangChain Document format**.

### Why this matters

Your data can come from:

* Text files
* PDFs
* Websites
* CSVs
* Databases
* Cloud storage
* APIs

But downstream components expect **ONE consistent structure**.

---

## 3️⃣ The LangChain `Document` Object (Core Concept)

Every loader outputs **Document objects**.

```python
from langchain.schema import Document

Document(
    page_content="Actual text content",
    metadata={
        "source": "file_path_or_url",
        "page": 3,
        ...
    }
)
```

### Two Mandatory Fields

| Field          | Purpose                                     |
| -------------- | ------------------------------------------- |
| `page_content` | Text used for embeddings & retrieval        |
| `metadata`     | Context (source, page number, row id, etc.) |

👉 Metadata becomes **very important during retrieval & debugging**.

---

## 4️⃣ Common Interface of All Document Loaders

All loaders follow the **same pattern**:

```python
loader = SomeLoader(...)
documents = loader.load()
```

Or for large datasets:

```python
documents = loader.lazy_load()
```

This uniform interface is a **major design strength** of LangChain.

---

## 5️⃣ Text Loader (Starting Point)

### When to use

* `.txt` files
* Logs
* Code snippets
* Transcripts
* Notes

### Example

```python
from langchain_community.document_loaders import TextLoader

loader = TextLoader(
    file_path="data/cricket.txt",
    encoding="utf-8"
)

documents = loader.load()

print(len(documents))
print(documents[0].page_content[:200])
print(documents[0].metadata)
```

### Output Behavior

* Usually **1 Document per file**
* Metadata contains file path

---

## 6️⃣ PDF Loaders (Important Distinction)

### ❌ PDFs are NOT simple text

PDFs can be:

* Text-based
* Scanned images
* Complex layouts

So **one loader does NOT fit all**.

---

### 6.1 PyPDF Loader (Most Common)

### Best for:

* Clean, text-based PDFs
* Books, docs, reports

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/ml_book.pdf")

documents = loader.load()

print(len(documents))          # One document per page
print(documents[0].metadata)  # page number, source
```

### Behavior

* **1 Document per page**
* Metadata includes:

  * `page`
  * `source`

---

### 6.2 When NOT to use PyPDF

❌ Scanned PDFs
❌ Tables-heavy layouts
❌ Image-based content

### Better Alternatives

* `PDFPlumberLoader`
* `UnstructuredPDFLoader`
* OCR-based loaders

---

## 7️⃣ Directory Loader (Bulk Loading)

### Problem it solves

Loading files **one-by-one doesn’t scale**.

### Directory Loader = Loader + Automation

```python
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    path="data/books",
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)

documents = loader.load()

print(f"Total documents: {len(documents)}")
```

### Key Points

* Uses **glob patterns**
* Can recursively scan folders
* Internally uses another loader

---

## 8️⃣ Eager vs Lazy Loading (VERY IMPORTANT)

### 8.1 Eager Loading (`load()`)

```python
documents = loader.load()
```

✔ Simple
❌ Loads everything into memory
❌ Dangerous for large datasets

---

### 8.2 Lazy Loading (`lazy_load()`)

```python
documents = loader.lazy_load()

for doc in documents:
    print(doc.metadata)
```

✔ Memory efficient
✔ Faster initial response
✔ Industry best practice for large data

### Rule of Thumb

| Data Size          | Method        |
| ------------------ | ------------- |
| Small              | `load()`      |
| Large / Production | `lazy_load()` |

---

## 9️⃣ Web Base Loader (Static Websites)

### Use Case

* Blogs
* Documentation pages
* News articles
* Static HTML pages

```python
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader(
    web_path="https://example.com/blog"
)

documents = loader.load()

print(documents[0].page_content[:300])
```

### Limitations

❌ JavaScript-heavy pages
❌ Dynamic content

### Solution for Dynamic Sites

* Selenium-based loaders
* Playwright loaders

---

## 🔟 CSV Loader (Structured Data)

### When to use

* Tabular data
* Analytics datasets
* Logs exported as CSV

### Behavior

* **1 row = 1 Document**

```python
from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="data/ads.csv"
)

documents = loader.load()

print(len(documents))
print(documents[0].page_content)
print(documents[0].metadata)
```

### Why this is powerful

* Enables **row-level querying**
* Perfect for business analytics with LLMs

---

## 1️⃣1️⃣ Lazy Loading with CSV (Large Files)

```python
for doc in loader.lazy_load():
    process(doc)
```

✔ Handles millions of rows safely

---

## 1️⃣2️⃣ Ecosystem of Document Loaders

LangChain supports **hundreds** of loaders:

| Category     | Examples             |
| ------------ | -------------------- |
| Cloud        | S3, GCS, Azure Blob  |
| Media        | YouTube, Audio       |
| Dev Tools    | GitHub, GitLab       |
| Data         | JSON, SQL, MongoDB   |
| Productivity | Notion, Google Drive |

👉 Same interface, same output.

---

## 1️⃣3️⃣ Writing a Custom Document Loader (Advanced)

### When needed

* Proprietary data
* Internal APIs
* Custom file formats

### Minimal Custom Loader

```python
from langchain.document_loaders.base import BaseLoader
from langchain.schema import Document

class MyCustomLoader(BaseLoader):
    def load(self):
        data = fetch_my_data()
        return [
            Document(
                page_content=item["text"],
                metadata={"source": "internal_api"}
            )
            for item in data
        ]
```

### Optional: Lazy Version

```python
    def lazy_load(self):
        for item in fetch_streaming_data():
            yield Document(
                page_content=item["text"],
                metadata={"source": "internal_api"}
            )
```

---

## 1️⃣4️⃣ Common Mistakes (Real-World)

❌ Using `load()` for huge datasets
❌ Assuming all PDFs behave the same
❌ Ignoring metadata
❌ Loading dynamic websites with static loaders
❌ Forgetting encoding in text files

---

## 1️⃣5️⃣ Best Practices (Industry Level)

✔ Always inspect `metadata`
✔ Prefer `lazy_load()` in production
✔ Choose PDF loader based on PDF type
✔ Use DirectoryLoader for scale
✔ Normalize data early (clean text)

---

## 🔚 Final Summary

* Document Loaders **standardize raw data**
* Output is always **Document objects**
* They are the **foundation of RAG**
* Lazy loading is **mandatory for scale**
* Once loaded → data is ready for splitting, embedding & retrieval

