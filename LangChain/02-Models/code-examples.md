# 💻 LangChain Models – Code Examples

This section contains **hands-on code examples** demonstrating how to use **LangChain Models** with:

* Closed-source models (OpenAI, Anthropic, Gemini)
* Open-source models (Hugging Face – API & Local)
* Embedding models
* Document similarity using cosine similarity

All examples follow **best practices** used in real-world GenAI projects.

---

## 📂 Project Setup

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

---

### 2️⃣ Install Dependencies

Create `requirements.txt`:

```txt
langchain
langchain-community
langchain-openai
langchain-anthropic
langchain-google-genai
huggingface-hub
transformers
python-dotenv
scikit-learn
numpy
sentence-transformers
torch
```

Install:

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Environment Variables (.env)

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_gemini_key
HUGGINGFACE_HUB_ACCESS_TOKEN=your_hf_token
```

Load once in code:

```python
from dotenv import load_dotenv
load_dotenv()
```

---


## 🧠 Language Models (LLM – Legacy)

> ⚠️ **Note**
> This example uses the **legacy LLM interface** in LangChain.
>
> 👉 Prefer **Chat Models** for all modern applications.

---

## OpenAI LLM (Instruction-Based – Legacy)

```python
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(
    model="gpt-3.5-turbo-instruct",
    temperature=0
)

result = llm.invoke("What is the capital of India")

print(result)
```

✅ Useful for:

* One-shot text generation
* Understanding classic LLM behavior
* Legacy LangChain codebases

❌ Not recommended for:

* Chatbots
* RAG
* Agents
* Multi-turn conversations

---

## 🧠 Language Models (Chat Models)

---

## 1️⃣ OpenAI Chat Model

```python
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7
)

response = llm.invoke("What is the capital of India?")
print(response.content)
```

✅ Best for:

* Q&A
* Explanations
* Production-grade chatbots

---

## 2️⃣ Anthropic Claude Chat Model

```python
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

llm = ChatAnthropic(
    model="claude-3-opus-20240229",
    temperature=0.5
)

response = llm.invoke("Explain LangChain in simple terms")
print(response.content)
```

✅ Known for:

* Safer responses
* Better long-form reasoning

---

## 3️⃣ Google Gemini Chat Model

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.6
)

response = llm.invoke("What is Generative AI?")
print(response.content)
```

✅ Strong multimodal and reasoning capabilities

---

## 🤖 Open-Source Models (Hugging Face)

---

## 4️⃣ Hugging Face Model via API (TinyLlama)

```python
from langchain_community.chat_models import ChatHuggingFace
from langchain_community.llms import HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm = ChatHuggingFace(
    llm=HuggingFaceEndpoint(
        repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        temperature=0.7
    )
)

response = llm.invoke("What is the capital of India?")
print(response.content)
```

✅ No local GPU required
❌ API latency possible

---

## 5️⃣ Hugging Face Model – Local Execution

```python
from transformers import pipeline
from langchain_community.chat_models import ChatHuggingFace
from langchain_community.llms import HuggingFacePipeline

pipeline_llm = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    max_new_tokens=200
)

llm = ChatHuggingFace(
    llm=HuggingFacePipeline(pipeline=pipeline_llm)
)

response = llm.invoke("Explain LLM vs Chat Model")
print(response.content)
```

✅ Full privacy
❌ Requires good CPU/GPU

---

## 🧮 Embedding Models

---

## 6️⃣ OpenAI Embeddings

```python
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    dimensions=1536
)

vector = embeddings.embed_query("Delhi is the capital of India")
print(len(vector))
```

✅ Industry standard
✅ High-quality embeddings

---

## 7️⃣ Open-Source Embeddings (Sentence Transformers)

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector = embeddings.embed_query("Delhi is the capital of India")
print(len(vector))
```

✅ Free
✅ Fast
❌ Slightly lower quality than OpenAI

---

## 🔍 Document Similarity (Cosine Similarity)

This example demonstrates how to:

* Generate embeddings using **OpenAI Embeddings**
* Compare documents using **cosine similarity**
* Retrieve the **most relevant document** for a given query

---

### 📌 Code Example

```python
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

load_dotenv()

# Initialize embedding model
embedding = OpenAIEmbeddings(
    model="text-embedding-3-large",
    dimensions=300
)

# Documents to compare
documents = [
    "Virat Kohli is an Indian cricketer known for his aggressive batting and leadership.",
    "MS Dhoni is a former Indian captain famous for his calm demeanor and finishing skills.",
    "Sachin Tendulkar, also known as the 'God of Cricket', holds many batting records.",
    "Rohit Sharma is known for his elegant batting and record-breaking double centuries.",
    "Jasprit Bumrah is an Indian fast bowler known for his unorthodox action and yorkers."
]

# User query
query = "tell me about bumrah"

# Generate embeddings
doc_embeddings = embedding.embed_documents(documents)
query_embedding = embedding.embed_query(query)

# Calculate cosine similarity
scores = cosine_similarity([query_embedding], doc_embeddings)[0]

# Get most similar document
index, score = sorted(
    list(enumerate(scores)),
    key=lambda x: x[1]
)[-1]

print(query)
print(documents[index])
print("similarity score is:", score)
```

---

### 🧠 How This Works (Simple Explanation)

1. **Convert documents into vectors** using OpenAI embeddings
2. **Convert the query into a vector**
3. **Compare query vector with all document vectors**
4. **Cosine similarity** finds the closest match
5. Document with the **highest score** is returned

---

### ✅ Why This Pattern Is Important

This logic is the **foundation of**:

* Retrieval-Augmented Generation (RAG)
* Chat with PDFs
* Knowledge-base chatbots
* Semantic search systems

Once this is clear, moving to **vector databases (FAISS, Chroma, Pinecone)** becomes very easy.
