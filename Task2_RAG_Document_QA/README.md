# Task 2 – RAG Document Question Answering System

## Project Overview

This project implements a Retrieval-Augmented Generation (RAG) system that answers questions based on uploaded PDF documents.

It uses LangChain, Google Gemini embeddings, ChromaDB, and Gemini Flash to retrieve relevant information and generate document-grounded answers.

## Technologies Used

- Python 3.13
- LangChain
- Google Gemini API
- ChromaDB
- PyPDF
- Recursive Character Text Splitter

## Project Structure

```text
Task2_RAG_Document_QA/
│
├── documents/
│   └── sample.pdf
│
├── chroma_db/
├── ingest.py
├── chat.py
├── requirements.txt
└── README.md
```

## Features

- Loads PDF documents.
- Extracts text from PDF pages.
- Splits documents into smaller chunks.
- Generates vector embeddings using Google Gemini.
- Stores document embeddings in ChromaDB.
- Retrieves relevant document chunks for user questions.
- Generates answers using Gemini.
- Displays source page numbers.
- Instructs the model not to use information outside the uploaded document.

## Installation

1. Install Python 3.13.
2. Create a virtual environment:

```bash
py -3.13 -m venv .venv
```

3. Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the parent project folder and add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key
```

Do not upload your API key to GitHub.

## How to Run

### Step 1: Add PDF documents

Place your PDF files inside the `documents` folder.

### Step 2: Ingest documents

```bash
python ingest.py
```

This extracts, chunks, embeds, and stores the documents in ChromaDB.

### Step 3: Start question answering

```bash
python chat.py
```

Enter questions about your uploaded PDF.

Type `exit` to stop the application.

## Example Question

**Question:** What is Artificial Intelligence?

**Answer:** Artificial Intelligence is a branch of computer science that focuses on creating machines capable of performing tasks that normally require human intelligence.

**Source Page:** 1

## Expected Result

The system retrieves relevant document content and generates answers based on the uploaded PDF. If the requested information is unavailable in the retrieved context, it is instructed to say that it could not find the information in the uploaded PDF.

## Author

Developed as part of the DAtheon Python Generative AI and LangChain Internship.