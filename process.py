import os
import json
import pdfplumber
import pandas as pd
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PDF_FOLDER = os.getenv("PDF_FOLDER", "pdf_files")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "extracted_data")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


chat = ChatGroq(model_name="llama3-3.3-70b-8192", groq_api_key=GROQ_API_KEY)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    extracted_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        return extracted_text.strip()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

def get_structured_json(pdf_text):
    """Extract structured table data from PDF text using LLM."""
    prompt = """
    Extract **all** tables from the given PDF text while maintaining the original structure.
    Ensure:
    1. Identify correct column headers and row labels.
    2. Store row values as JSON objects.
    3. Include a total row summing up each column.
    **Return only valid JSON.**
    """
    try:
        response = chat.invoke([
            SystemMessage(content="You are an AI assistant that extracts structured data from PDFs."),
            HumanMessage(content=prompt + "\n\nExtracted PDF Text:\n" + pdf_text)
        ])
        return extract_json_from_response(response.content.strip())
    except Exception as e:
        print(f"Error processing with LLM: {e}")
        return None

def extract_json_from_response(response_text):
    """Extract the JSON portion from the LLM response."""
    try:
        start = response_text.find("[")
        end = response_text.rfind("]") + 1
        json_str = response_text[start:end]
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def save_json(data, filename):
    """Save extracted data as JSON."""
    json_path = os.path.join(OUTPUT_FOLDER, filename)
    try:
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f"Saved: {json_path}")
    except Exception as e:
        print(f"Error saving JSON file: {e}")

def json_to_dataframe(json_data):
    """Convert JSON data to Pandas DataFrame with a total row."""
    df = pd.DataFrame(json_data)
    total_row = {col: df[col].sum() if df[col].dtype in ['int64', 'float64'] else '' for col in df.columns}
    total_row[df.columns[0]] = "Total"
    return pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)
