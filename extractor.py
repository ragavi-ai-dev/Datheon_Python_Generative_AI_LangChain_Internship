
import os
from dotenv import load_dotenv
from google import genai
from schemas import ResumeData, InvoiceData
# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found!")

# Connect to Gemini
client = genai.Client(api_key=api_key)


def extract_resume(resume_text):

    prompt = f"""
    Extract information from this resume.

    Return these fields:
    name, email, phone, skills, education, experience.

    If information is missing, use an empty value
    or an empty list.

    Resume text:
    {resume_text}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": ResumeData.model_json_schema()
        }
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    result = ResumeData.model_validate_json(response.text)

    return result

def extract_invoice(invoice_text):

    prompt = f"""
    Extract information from this invoice.

    Return these fields:
    invoice_number, customer_name, total_amount, date.

    If information is missing, use an empty value
    or zero for total_amount.

    Invoice text:
    {invoice_text}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": InvoiceData.model_json_schema()
        }
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    result = InvoiceData.model_validate_json(response.text)

    return result


if __name__ == "__main__":

    sample_resume = """
    Name: Arun Kumar
    Email: arun@example.com
    Phone: 9876543210
    Skills: Python, Java, SQL
    Education: B.Tech Computer Science
    Experience: Python Developer Intern
    """

    result = extract_resume(sample_resume)

    print("\nAI RESUME EXTRACTION RESULT")
    print("=" * 40)

    print(result.model_dump_json(indent=4))
    
    sample_invoice = """
    Invoice Number: INV001
    Customer Name: Ragavi
    Total Amount: 5000
    Date: 12-11-2026
    """

    invoice_result = extract_invoice(sample_invoice)

    print("\nAI INVOICE EXTRACTION RESULT")
    print("=" * 40)

    print(invoice_result.model_dump_json(indent=4))

