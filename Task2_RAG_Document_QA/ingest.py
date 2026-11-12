
from pathlib import Path
import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


# Project folders
BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Load the API key from Task 1's .env file
load_dotenv(BASE_DIR.parent / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in the parent .env file!")


def main():

    print("\nRAG DOCUMENT INGESTION")
    print("=" * 40)

    # Step 1: Load PDF documents
    documents = []

    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in the documents folder.")
        return

    for pdf_file in pdf_files:
        print(f"Reading: {pdf_file.name}")

        loader = PyPDFLoader(str(pdf_file))
        documents.extend(loader.load())

    print(f"\nTotal pages loaded: {len(documents)}")

    # Step 2: Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    # Step 3: Generate Gemini embeddings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview",
        google_api_key=api_key
    )

    # Step 4: Store chunks in ChromaDB
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name="rag_documents"
    )

    print("\nPDF successfully stored in ChromaDB!")
    print("Ingestion completed successfully.")


if __name__ == "__main__":
    main()
