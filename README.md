# AI Resume and Invoice Extraction

## Project Description
This project uses Google's Gemini AI to extract structured information from resume and invoice text.

## Features
- Extracts information from resumes.
- Extracts information from invoices.
- Uses Pydantic models to validate extracted data.
- Saves extracted information as JSON files.

## Technologies Used
- Python
- Google Gemini API
- Pydantic
- python-dotenv

## Project Structure
```text
DAtheon_task1/
├── .env
├── .gitignore
├── schemas.py
├── extractor.py
├── main.py
└── output/
```

## Setup Instructions

1. Install Python.
2. Install the required packages:

```bash
pip install google-genai pydantic python-dotenv
```

3. Create a `.env` file in the project folder and add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
```

4. Run the project:

```bash
python main.py
```

5. Select Resume Extraction or Invoice Extraction.
6. Paste the document text and type `END` on a new line.
7. The extracted information will be saved as a JSON file inside the `output` folder.

## Note
Keep your Gemini API key private. Do not upload your `.env` file to GitHub.