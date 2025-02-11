import os
import pandas as pd
from process import extract_text_from_pdf, get_structured_json, save_json, json_to_dataframe
from dotenv import load_dotenv


load_dotenv()

PDF_FOLDER = os.getenv("PDF_FOLDER", "pdf_files")
OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "extracted_data")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def main():
    """Main function to process all PDFs in the folder."""
    pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
    if not pdf_files:
        print("No PDFs found in 'pdf_files' folder.")
        return

    print(f"Processing {len(pdf_files)} PDFs...")

    with pd.ExcelWriter(os.path.join(OUTPUT_FOLDER, "extracted_data.xlsx"), engine="xlsxwriter") as writer:
        for pdf_file in pdf_files:
            pdf_path = os.path.join(PDF_FOLDER, pdf_file)
            print(f"Extracting text from {pdf_file}...")

            pdf_text = extract_text_from_pdf(pdf_path)
            if not pdf_text:
                print(f"No text found in {pdf_file}, skipping...")
                continue

            print(f"Processing {pdf_file} with LLM...")
            json_data = get_structured_json(pdf_text)
            if not json_data:
                print(f"Failed to get structured data for {pdf_file}, skipping...")
                continue

            json_filename = f"{os.path.splitext(pdf_file)[0]}.json"
            save_json(json_data, json_filename)

            df = json_to_dataframe(json_data)
            sheet_name = os.path.splitext(pdf_file)[0][:30]  
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"All PDFs processed. Data saved in '{OUTPUT_FOLDER}/extracted_data.xlsx'")

if __name__ == "__main__":
    main()
