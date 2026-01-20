# 📘 **YouTube Chatbot Using LangChain + Advanced RAG**

---

# 1️⃣ Introduction: What Exactly Are We Building?

We are building a **YouTube Chatbot** where a user can:

* Paste a **YouTube video link**
* Ask **any question** about the video
* Get responses **grounded in the actual video transcript**
* Without watching the entire video

This system uses **RAG (Retrieval-Augmented Generation)** implemented using **LangChain** in Python.

---

# 2️⃣ Why YouTube + RAG?

YouTube videos (especially podcasts, lectures, tutorials) are long.
People don’t want to scrub through 2+ hours to find:

* Whether a topic is discussed
* The explanation of a specific concept
* A structured summary
* Key takeaways

A RAG system solves this by:

1. Fetching transcript
2. Splitting transcript
3. Converting chunks to embeddings
4. Storing them in a vector DB
5. Retrieving relevant chunks
6. Answering based on retrieved context

---

# 3️⃣ High-Level Architecture (End-to-End Flow)

```
YouTube Video URL
        ↓
YouTube Transcript API
        ↓
Raw Transcript (Text)
        ↓
Text Splitter → Chunks
        ↓
Embeddings (OpenAI)
        ↓
Vector Store (FAISS)
        ↓
Retriever (Semantic Search)
        ↓
Context Builder
        ↓
Prompt Template
        ↓
LLM (OpenAI) → Grounded Answer
```

This pipeline is fully automated using **LangChain Runnable Chains**.

---

# 4️⃣ Step-by-Step 

## 🔹 **Step 1 – Load YouTube Transcript**

We use **YouTube Transcript API** (more stable than LangChain loader).

Process:

* Extract video ID from URL
* Load transcript (English/Hindi)
* API returns list of segments → Combine into single text string

**Important Notes:**

* Some videos have auto-generated captions → may contain noise
* If transcript is missing: fallback to different language
* For production: add a transcript caching layer

---

## 🔹 **Step 2 – Text Splitting (Chunking)**

Long transcript → must be converted into meaningful chunks.

We use:

### **RecursiveCharacterTextSplitter**

Reason:

* Smart fallback splitting (paragraph → sentence → word)
* Prevents cutting mid-sentence unnecessarily
* Works well for long-form transcripts

Recommended parameters:

* **chunk_size = 1000**
* **chunk_overlap = 200**

Why overlap?

* Ensures sentence continuity
* Improves retrieval accuracy

Better approaches for advanced RAG are discussed later.

---

## 🔹 **Step 3 – Embedding & Vector Store**

Next, convert chunks to embeddings (numerical vectors).

### Embeddings:

* OpenAI model (e.g., `text-embedding-3-small` or `large`)
* Embedding quality heavily affects retrieval accuracy

### Vector Store:

* FAISS (local, fast, free)
* Efficient similarity search

Workflow:

* Convert chunks → vectors
* Store in FAISS index
* Map each vector to its chunk

---

## 🔹 **Step 4 – Build a Retriever**

Retriever = the “brain” that fetches relevant chunks.

We use:

* **similarity search**
* return top **4** chunks (default)

Better strategies later:

* Hybrid search
* MMR
* Re-ranking
* Multi-query retrieval

---

## 🔹 **Step 5 – Build Prompt (Argumentation)**

Prompt instructs LLM to:

* Read retrieved context
* Answer question only from context
* Avoid hallucination
* Say “I don’t know” if answer not present

This is crucial for safety, grounding, and correctness.

Example structure:

```
Use only the provided transcript excerpt to answer.
If unsure, say you don't know.
Transcript:
{context}

Question:
{question}

Answer:
```

---

## 🔹 **Step 6 – LLM Generation**

Finally:

* Inject prompt
* Send to OpenAI LLM
* Parse the output

Key idea:
**LLM should NOT use its internal knowledge.
It must rely only on transcript context.**

---

## 🔹 **Step 7 – Automating the Pipeline using LangChain Chains**

LangChain provides:

* RunnableParallel → Run retriever & question in parallel
* RunnableLambda → Custom transformations
* RunnableSequence → End-to-end pipeline

Final chain:

```
User Input → Retriever → Context → Prompt → LLM → Answer
```

A single function call handles the whole RAG process.

---

# 5️⃣ **Fully Structured YouTube RAG Code**

```python
"""
YouTube RAG Chatbot using LangChain
-----------------------------------
This script:
1. Fetches a YouTube transcript
2. Splits transcript into chunks
3. Creates OpenAI embeddings
4. Stores them in FAISS vector DB
5. Uses a retriever for semantic search
6. Builds prompt → LLM → answer pipeline
7. Allows full conversational querying
"""

# ---------------------------------------------------
# 1. INSTALL DEPENDENCIES
# ---------------------------------------------------
# Run in Colab:
# !pip install youtube-transcript-api langchain openai faiss-cpu python-dotenv tiktoken


# ---------------------------------------------------
# 2. IMPORTS & ENVIRONMENT
# ---------------------------------------------------
import os
from dotenv import load_dotenv

from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# Load .env file (if exists)
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or "YOUR_KEY_HERE"


# ---------------------------------------------------
# 3. UTILS: Extract Video ID
# ---------------------------------------------------
def get_video_id(url: str) -> str:
    """Extract video ID from a YouTube URL."""
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    raise ValueError("Invalid YouTube URL")


# ---------------------------------------------------
# 4. FETCH TRANSCRIPT
# ---------------------------------------------------
def fetch_youtube_transcript(url: str, languages=["en", "hi"]):
    """
    Fetches transcript using youtube-transcript-api.
    Falls back to auto-generated captions if human subtitles are unavailable.
    """
    vid = get_video_id(url)

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(vid)
    except Exception:
        raise Exception("Transcript not available for this video.")

    # Try all language preferences
    transcript_data = None
    for lang in languages:
        try:
            transcript_data = transcript_list.find_transcript([lang])
            break
        except:
            continue

    # Fallback: Use any auto-generated transcript
    if transcript_data is None:
        transcript_data = transcript_list.find_transcript(
            transcript_list._transcripts_by_language.keys()
        )

    # Convert segments → single string
    transcript_text = " ".join([s["text"] for s in transcript_data.fetch()])
    return transcript_text


# ---------------------------------------------------
# 5. TEXT SPLITTING (Chunking)
# ---------------------------------------------------
def split_into_chunks(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    return splitter.create_documents([text])


# ---------------------------------------------------
# 6. BUILD VECTOR STORE (FAISS)
# ---------------------------------------------------
def create_vector_store(chunks):
    """
    Creates embeddings + FAISS vector store.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store


# ---------------------------------------------------
# 7. PROMPT TEMPLATE
# ---------------------------------------------------
prompt_template = PromptTemplate(
    template="""
You are a transcript-based assistant. Answer ONLY from the given transcript context.
If answer not present in context, say "I don't know".

Context:
--------
{context}

Question:
---------
{question}

Answer:
""",
    input_variables=["context", "question"]
)


# ---------------------------------------------------
# 8. HELPER: Format Retrieved Docs → Context
# ---------------------------------------------------
def format_docs(docs):
    """Combine retrieved document text into final context."""
    return "\n\n".join([doc.page_content for doc in docs])


# ---------------------------------------------------
# 9. BUILD THE FULL RAG CHAIN (LangChain Runnable Graph)
# ---------------------------------------------------
def build_rag_chain(vector_store):
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    parallel_chain = RunnableParallel({
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    })

    main_chain = (
        parallel_chain
        | prompt_template
        | llm
        | StrOutputParser()
    )

    return main_chain


# ---------------------------------------------------
# 10. FULL PIPELINE FUNCTION
# ---------------------------------------------------
def youtube_rag_answer(video_url: str, question: str):
    """
    Complete pipeline:
    transcript → chunks → embeddings → retriever → LLM answer
    """
    print("🔹 Fetching transcript...")
    transcript_text = fetch_youtube_transcript(video_url)

    print(f"🔹 Transcript length: {len(transcript_text)} characters")

    print("🔹 Splitting into chunks...")
    chunks = split_into_chunks(transcript_text)

    print(f"🔹 Created {len(chunks)} chunks")

    print("🔹 Creating vector store (FAISS)...")
    vector_store = create_vector_store(chunks)

    print("🔹 Building RAG chain...")
    rag_chain = build_rag_chain(vector_store)

    print("🔹 Generating answer...")
    return rag_chain.invoke(question)


# ---------------------------------------------------
# 11. EXAMPLE USAGE
# ---------------------------------------------------
if __name__ == "__main__":
    VIDEO_URL = "https://youtu.be/Gfr50f6ZBvo"
    QUESTION = "Is nuclear fusion discussed in this video? If yes, what was said?"

    answer = youtube_rag_answer(VIDEO_URL, QUESTION)
    print("\nFINAL ANSWER:\n", answer)
```

---

# 6️⃣ System Limitations (Important for Real Projects)

1. Transcript may have errors (auto-generated captions).
2. If transcript is unavailable → can't proceed.
3. Chunking may split semantic boundaries (resolve via semantic chunkers).
4. FAISS is local → not scalable across distributed systems.
5. Retrieval quality depends on:

   * embedding quality
   * chunk size
   * query rewrite
6. LLM token limits restrict context size.

---

# 7️⃣ Advanced RAG Concepts 

This is where you go beyond the simple implementation.

## 🧠 **1. Query Transformation Techniques**

* Multi-query rewriting
* Query expansion
* Domain-aware routing
* Keyword + semantic hybrid search

## 🧠 **2. Advanced Chunking**

* Semantic chunking (uses embeddings to find boundaries)
* Topic-aware chunking
* Scene-based segmentation (in multimodal RAG)

## 🧠 **3. Retrieval Enhancements**

* LLM-based re-ranking (Cross-encoder style)
* MMR (Minimal Marginal Relevance)
* Contextual compression retrievers

## 🧠 **4. Better Vector Stores**

* Pinecone
* Weaviate
* Qdrant
* Milvus

These offer:

* Scalability
* Hybrid search
* Sharding
* Filtering (metadata-based search)

## 🧠 **5. Prompt Engineering for RAG**

* Instruction grounding
* Template with examples
* Tight context windows
* Avoid overloading tokens

## 🧠 **6. Answer Safety**

* Add citations (source chunk references)
* Add disclaimers or fallback messages
* Ensure “I don’t know” behavior

## 🧠 **7. Multimodal RAG**

Transcripts + images + slides + screen content
Useful for:

* Educational channels
* Coding walkthrough videos
* Product demos

## 🧠 **8. Agentic RAG**

Agents can:

* Browse web
* Verify answers
* Call APIs
* Retrieve external data

Useful for YouTube chatbots that:

* Find similar videos
* Compare two videos
* Provide enriched summaries

## 🧠 **9. Memory-Augmented RAG**

* Stores user preferences
* Remembers past queries
* Provides long-term conversational context

Ideal for:

* Personalized learning
* Course-based video chatbots

---

# 8️⃣ Real-World UX/UI Enhancements

### **A. Streamlit App**

* Upload multiple URLs
* Chat window
* Transcript preview
* Chunk inspector

### **B. Chrome Extension**

* Works directly on YouTube
* “Chat with this video” sidebar
* Highlights relevant sections

### **C. Enterprise Features**

* Logging & monitoring
* Rate limiting
* User-level personalization
* Secure API endpoints

---

# 9️⃣ Potential Improvements (Production Level)

| Area          | Upgrade                                             |
| ------------- | --------------------------------------------------- |
| Chunk Quality | Use semantic chunking or LLM-based summarization    |
| Retrieval     | Hybrid + re-ranking + MMR                           |
| Context       | Auto-context selection based on token limits        |
| Search        | Support multi-lingual transcripts                   |
| Accuracy      | Use Guardrails + hallucination detection            |
| Speed         | Cache embeddings + FAISS index                      |
| Scaling       | Move to Pinecone / Qdrant                           |
| Evaluation    | Use RAGAS metrics (faithfulness, recall, relevancy) |

---
