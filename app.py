

import os
import json
import pdfplumber
import pandas as pd
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PDF_FOLDER = os.getenv("PDF_FOLDER", "pdf_files")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "extracted_data")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize LLM model
chat = ChatGroq(model_name="llama3-70b-8192", groq_api_key=GROQ_API_KEY)

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
    """Send the extracted PDF text directly to the LLM for processing."""
    prompt = """
    Extract **all** tables from the given PDF while maintaining the original structure.
    Ensure:
    1. Identify correct column headers and row labels.
    2. Store row values as JSON objects.
    3. Return only valid JSON.
    """

    try:
        response = chat.invoke([
            SystemMessage(content="You are an AI assistant that extracts structured data from PDFs."),
            HumanMessage(content=prompt + "\n\nExtracted PDF Text:\n" + pdf_text)
        ])

        raw_response = response.content.strip()
        print(f"Raw LLM Response:\n{raw_response}\n")  # Log the raw response

        # Check if the response contains a description followed by the JSON data
        if "Here is the extracted table in JSON format" in raw_response:
            json_start_index = raw_response.find("[")  # Find the start of JSON
            json_end_index = raw_response.rfind("]") + 1  # Find the end of JSON
            json_str = raw_response[json_start_index:json_end_index]
            return json.loads(json_str)  # Try parsing the extracted JSON part
        else:
            print("No JSON found in LLM response.")
            return None

    except Exception as e:
        print(f"Error processing with LLM: {e}")
        return None

def extract_json_from_response(response_text):
    """Extract the JSON portion from the LLM response."""
    try:
        # Try to parse the JSON string
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
    """Convert JSON data to Pandas DataFrame."""
    df = pd.DataFrame(json_data)
    return df

def process_pdf(pdf_file):
    """Process a single PDF file."""
    pdf_path = os.path.join(PDF_FOLDER, pdf_file)
    print(f"Extracting text from {pdf_file}...")

    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(pdf_path)
    if not pdf_text:
        print(f"No text found in {pdf_file}, skipping...")
        return

    print(f"Processing {pdf_file} with LLM...")
    
    # Get structured JSON from the LLM
    json_data = get_structured_json(pdf_text)
    if not json_data:
        print(f"Failed to get structured data for {pdf_file}, skipping...")
        return

    # Save JSON data
    json_filename = f"{os.path.splitext(pdf_file)[0]}.json"
    save_json(json_data, json_filename)

    # Convert JSON to Excel
    df = json_to_dataframe(json_data)
    excel_filename = f"{os.path.splitext(pdf_file)[0]}.xlsx"
    excel_path = os.path.join(OUTPUT_FOLDER, excel_filename)
    df.to_excel(excel_path, index=False)
    print(f"Excel file saved: {excel_path}")

def main():
    """Main function to process all PDFs in the folder."""
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
    if not pdf_files:
        print("No PDFs found in 'pdf_files' folder.")
        return

    print(f"Processing {len(pdf_files)} PDFs...")
    for pdf_file in pdf_files:
        process_pdf(pdf_file)
    
    print("All PDFs processed successfully.")

if __name__ == "__main__":
    main()




