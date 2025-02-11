
# PDF Processing Project

## Overview

This project is designed to process and extract structured data from PDFs. The core functionality is built around using `pdfplumber` for text extraction and `langchain` for invoking an LLM model (via `Groq`) to parse the data into structured JSON format. The extracted data is then saved into both JSON and Excel formats for further processing.

## Features

- Extracts text and tables from PDFs.
- Processes multiple PDFs and saves data in structured JSON format.
- Converts extracted data into an Excel sheet using Pandas.
- Handles errors gracefully and logs them for further review.

## Requirements

- Python 3.8+
- A `Groq` API key for LLM processing (configured via environment variables).
- Required Python packages listed in `requirements.txt`.

## Installation

### Step 1: Clone the repository

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/hassanali167/pdf-processing.git
cd pdf-processing
```

### Step 2: Set up a virtual environment

To create a virtual environment for the project, use the following commands:

```bash
# Install virtualenv if it's not already installed
pip install virtualenv

# Create a new virtual environment
virtualenv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install dependencies

Install the required dependencies using `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 4: Set up environment variables

You will need to set up the following environment variables:

- **GROQ_API_KEY**: Your `Groq` API key for LLM processing.
- **PDF_FOLDER**: The folder where the PDFs are located (default is `pdf_files`).
- **OUTPUT_FOLDER**: The folder where the output files (JSON and Excel) will be saved (default is `extracted_data`).

Create a `.env` file in the project root and add the variables:

```
GROQ_API_KEY=your_groq_api_key
PDF_FOLDER=path_to_your_pdf_folder
OUTPUT_FOLDER=path_to_output_folder
```

### Step 5: Run the script

After the setup, you can run the script to process the PDFs:

```bash
python app.py
```

This will process all the PDFs in the specified folder and save the structured data as JSON and Excel files in the output folder.

## File Structure

- **app.py**: Main script to extract data from PDFs and process them using the LLM.
- **requirements.txt**: List of required Python packages for the project.
- **.env**: Environment variables for configuration.
- **pdf_files/**: Folder containing the PDF files to be processed.
- **extracted_data/**: Folder where the extracted data (JSON and Excel) will be saved.

## Troubleshooting

- Ensure your `GROQ_API_KEY` is correct and has the required access.
- If you encounter any errors regarding dependencies, make sure your virtual environment is active and all packages are correctly installed.

## License

This project is licensed under the MIT License.

---

### `requirements.txt`

Based on the libraries used in your code, here is the `requirements.txt` file:

```txt
pdfplumber==0.6.0
pandas==2.0.1
langchain==0.0.145
langchain_groq==0.0.1
python-dotenv==0.21.0
openai==0.27.0
```

```bash
pip install -r requirements.txt
```
---

Let me know if you need any additional modifications or if something needs further clarification!