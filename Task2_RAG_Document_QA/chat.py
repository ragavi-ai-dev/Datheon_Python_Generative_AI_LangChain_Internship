
from pathlib import Path
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


# Project paths
BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"

# Load Gemini API key from Task 1's .env file
load_dotenv(BASE_DIR.parent / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")


# Initialize embedding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    google_api_key=api_key
)

# Connect to existing ChromaDB
vector_store = Chroma(
    collection_name="rag_documents",
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR)
)

# Create retriever
retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=api_key,
    temperature=0
)


def ask_question(question):

    print("\nSearching your PDF...")

    # Retrieve relevant document chunks
    documents = retriever.invoke(question)

    if not documents:
        print("No relevant information found in the PDF.")
        return

    # Prepare context from retrieved documents
    context = "\n\n".join(
        document.page_content for document in documents
    )

    # Collect source page numbers
    pages = sorted({
        document.metadata.get("page", 0) + 1
        for document in documents
    })

    # Strict question-answering prompt
    prompt = f"""
You are a document question-answering assistant.

Answer the question ONLY using the information in the
provided document context.

If the answer is not available in the context, say:
"I could not find this information in the uploaded PDF."

Do not use outside knowledge or make up information.

DOCUMENT CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    # Generate answer
    response = llm.invoke(prompt)

    print("\nANSWER:")
    answer = response.content

if isinstance(answer, list):
    answer = "\n".join(
        item.get("text", "")
        for item in answer
        if isinstance(item, dict) and item.get("type") == "text"
    )

print(answer)
    print("\nSOURCE PAGES:")
    print(pages)


def main():

    print("\nAI DOCUMENT QUESTION ANSWERING SYSTEM")
    print("=" * 45)

    print("Ask questions about your uploaded PDF.")
    print("Type 'exit' to stop.")

    while True:

        question = input("\nEnter your question: ")

        if question.lower().strip() == "exit":
            print("Thank you for using the RAG system!")
            break

        if not question.strip():
            print("Please enter a question.")
            continue

        ask_question(question)


if __name__ == "__main__":
    main()
