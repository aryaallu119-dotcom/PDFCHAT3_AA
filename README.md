# 📄 AI-Powered PDF Chatbot using RAG

## Overview

This project is an AI-powered PDF Chatbot that allows users to upload PDF documents and ask questions about their content. The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded PDF and generate accurate responses using a Large Language Model (LLM).

The application combines a React frontend, Node.js backend, and FastAPI-based AI service to provide an interactive question-answering experience over PDF documents.

---

## Architecture

```text
React Frontend
       │
       ▼
Node.js + Express Backend
       │
       ▼
FastAPI AI Service
       │
       ├── PDF Processing (PyPDF)
       ├── Text Splitting
       ├── Embedding Generation
       ├── ChromaDB Vector Store
       ├── Retrieval Pipeline
       └── Groq LLM
```

---

## Features

* Upload PDF documents
* Extract text from PDFs
* Intelligent text chunking
* Generate embeddings using Hugging Face models
* Store embeddings in ChromaDB
* Semantic similarity search
* Retrieval-Augmented Generation (RAG)
* Ask questions about uploaded PDFs
* Context-aware responses
* Microservice architecture using Node.js and FastAPI

---

## Tech Stack

### Frontend

* React.js

### Backend

* Node.js
* Express.js
* Multer

### AI Service

* FastAPI
* LangChain

### Vector Database

* ChromaDB

### Embeddings

* Hugging Face Embeddings
* Sentence Transformers

### LLM

* Groq API

### PDF Processing

* PyPDF

---

## Project Structure

```text
project-root/
│
├── public/
│
├── src/
│   ├── components/
│   │   ├── Chatpage/
│   │   │   ├── index.js
│   │   │   └── styledComponents.js
│   │   │
│   │   ├── HomePage/
│   │   │   ├── index.js
│   │   │   └── styledComponents.js
│   │   │
│   │   ├── Message/
│   │   │   ├── index.js
│   │   │   └── styledComponents.js
│   │   │
│   │   └── NotFound/
│   │
│   ├── App.js
│   ├── App.css
│   ├── index.css
│   └── index.js
│
├── backend/
│   │
│   ├── Uploads/
│   │
│   ├── python_services/
│   │   │
│   │   ├── Rag_service/
│   │   │   ├── applogic.py
│   │   │   ├── main.py
│   │   │   └── app.env
│   │   │
│   │   ├── chroma_langchain_db/
│   │   ├── **pycache**/
│   │   └── .cache/
│   │
│   ├── server.js
│   ├── package.json
│   └── package-lock.json
│
└── README.md

```

---

## Installation Guide

### 1. Clone Repository

```bash
git clone <repository-url>
cd <project-folder>
```

---

## Frontend Setup

### Install Dependencies

```bash
npm install
```

### Start React Application

```bash
npm start
```

Frontend runs on:

```text
http://localhost:3000
```

---

## Node.js Backend Setup

Move to backend folder:

```bash
cd backend
```

### Install Dependencies

```bash
npm install
```

### Install Additional Packages

```bash
npm install express multer axios cors
```

### Start Backend Server

```bash
node server.js
```

or

```bash
npx nodemon server.js
```

Backend runs on:

```text
http://localhost:5000
```

---

## FastAPI Setup

Move to Python service folder:

```bash
cd python_service
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

---

### Install Required Packages

```bash
pip install fastapi
pip install uvicorn
pip install langchain
pip install chromadb
pip install pypdf
pip install sentence-transformers
pip install langchain-community
pip install langchain-huggingface
pip install langchain-text-splitters
pip install groq
```

---

### Alternative Installation

```bash
pip install fastapi uvicorn langchain chromadb pypdf sentence-transformers langchain-community langchain-huggingface langchain-text-splitters groq
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

## Start FastAPI Server

```bash
python -m uvicorn main:app --reload --port 8000
```

FastAPI runs on:

```text
http://localhost:8000
```

---

## API Endpoints

### Upload PDF

```http
POST /upload
```

Uploads PDF to the server.

---

### Process PDF

```http
POST /process
```

Receives PDF path and generates embeddings.

---

### Ask Questions

```http
POST /query
```

Accepts user questions and returns AI-generated answers using RAG.

---

## Workflow

1. User uploads PDF.
2. Node.js saves PDF.
3. PDF path is sent to FastAPI.
4. PyPDF extracts text.
5. LangChain Text Splitter creates chunks.
6. Hugging Face generates embeddings.
7. ChromaDB stores embeddings.
8. User asks a question.
9. Retriever fetches relevant chunks.
10. Groq LLM generates an answer.
11. Response is displayed in React.

---

## Future Enhancements

* Multi-PDF support
* User authentication
* Chat history
* PDF summarization
* Source citations
* Conversation memory
* Cloud deployment
* Role-based access

---

## Learning Outcomes

This project demonstrates:

* React Development
* REST APIs
* Node.js Backend Development
* FastAPI Development
* Microservices Architecture
* Vector Databases
* Retrieval-Augmented Generation (RAG)
* Large Language Model Integration
* AI Application Development

```

Made with ❤️ using React, Node.js, FastAPI, LangChain, ChromaDB, Hugging Face Embeddings, and Groq.
```
