# Task 3 – AI Agent using LangChain and Gemini

## Project Overview
This project is an AI Agent developed using LangChain and Google's Gemini model. It can understand user queries and automatically select the appropriate tools to complete tasks.

## Features
The AI Agent includes three tools:

1. **Web Search** – Searches the web for information using DuckDuckGo.
2. **Calculator** – Performs mathematical calculations using Python.
3. **Local File Reader** – Reads supported local files such as TXT, MD, CSV, and JSON.

## Technologies Used
- Python
- LangChain
- Google Gemini
- DuckDuckGo Search
- python-dotenv

## Project Structure
```text
Task3_AI_Agent/
│
├── main.py
├── tools.py
├── sample.txt
├── uuid_utils/
│   ├── __init__.py
│   └── compat.py
└── README.md
```

## Setup Instructions

1. Clone or download the project.
2. Create and activate a Python virtual environment.
3. Install the required dependencies.
4. Configure your Gemini API key in the `.env` file in the parent project folder.

Example `.env` entry:

```env
GEMINI_API_KEY=your_api_key_here
```

Never upload your actual API key to GitHub.

## Run the Project

Run the following command from the Task3_AI_Agent folder:

```bash
python main.py
```

## Example Queries

```text
Calculate (250 * 4) + 150
```

```text
Read the contents of sample.txt
```

```text
Search the web for Python 3.13 release information
```

```text
Read sample.txt, calculate 125 * 8, and search the web for Python 3.13 information. Combine all three results.
```

## Expected Result
The AI Agent automatically selects and invokes the required tools and combines their results into a clear response.

## Author
Developed as part of the DAtheon Internship Task 3.
