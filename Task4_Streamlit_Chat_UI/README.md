# Task 4: Streamlit Chat UI with AI Agent

## Project Description
This project develops an interactive AI-powered chat interface using Streamlit and LangChain. It connects a Gemini AI Agent with three useful tools to answer user questions.

## Features
- Interactive Streamlit chat interface
- Gemini AI integration
- Chat history using Streamlit session state
- Web Search tool
- Calculator tool
- Local File Reader tool
- Asynchronous token streaming implementation

## Technologies Used
- Python
- Streamlit
- LangChain
- Google Gemini API
- DuckDuckGo Search

## Project Structure
```text
Task4_Streamlit_Chat_UI/
│
├── app.py
├── tools.py
├── sample.txt
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository.
2. Navigate to the project folder.
3. Create and activate a virtual environment.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the parent project directory and add:

```text
GEMINI_API_KEY=your_api_key_here
```

Never upload your actual API key to GitHub.

## Run the Application

```bash
python -m streamlit run app.py
```

## Available Tools

1. **Web Search:** Searches the internet for information.
2. **Calculator:** Evaluates mathematical expressions.
3. **Local File Reader:** Reads supported TXT, Markdown, CSV, and JSON files.

## Internship
DAtheon Python Generative AI & LangChain Internship – Task 4