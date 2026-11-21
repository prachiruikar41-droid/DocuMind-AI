# 📚 DocuMind AI – Ask Questions from Your PDF

DocuMind AI is a simple AI-powered Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions based on their content.

The application extracts text from uploaded PDFs, divides it into chunks, generates embeddings, retrieves relevant information, and uses a locally running Large Language Model (LLM) to generate answers.

## ✨ Features

- Upload PDF documents
- Extract text from PDF files
- Split text into chunks
- Generate embeddings using Nomic Embeddings
- Retrieve relevant chunks using Cosine Similarity
- Generate answers using Gemma LLM
- View retrieved context
- User-friendly Streamlit interface
- Runs locally using Ollama

## 🛠️ Tech Stack

- Python
- Streamlit
- Ollama
- Gemma 3 (4B)
- Nomic Embeddings
- PyPDF
- Requests

## ⚙️ How It Works

1. Upload a PDF document.
2. Extract text from the PDF.
3. Split extracted text into smaller chunks.
4. Generate embeddings for each chunk.
5. Convert the user's question into an embedding.
6. Retrieve the most relevant chunks using cosine similarity.
7. Send the retrieved context and question to Gemma.
8. Display the generated answer.

## 🧠 RAG Architecture

PDF Upload → Text Extraction → Chunking → Embeddings → Similarity Search → Context Retrieval → LLM → Answer

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

### 2. Navigate to the project folder

```bash
cd DocuMind_AI_RAG_Project
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Install Ollama

Download Ollama: https://ollama.com

### 7. Pull the required models

```bash
ollama pull gemma3:4b
ollama pull nomic-embed-text
```

### 8. Run the application

```bash
python -m streamlit run app.py
```

Open the application in your browser:

http://localhost:8501

## 📂 Project Structure

```text
DocuMind_AI_RAG_Project/
│
├── app.py
├── rag.py
├── embeddings.py
├── requirements.txt
├── README.md
└── .venv/
```

## 🎯 Project Goal

The goal of DocuMind AI is to make information extraction from PDF documents easier by allowing users to interact with their documents through natural language questions.

## 👩‍💻 Developed By

A Python and AI project built to explore Retrieval-Augmented Generation (RAG), embeddings, semantic search, and Large Language Models.
