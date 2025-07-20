# PDF Summarizer Chatbot App
This is a Streamlit-based web application that allows users to upload one or more PDF documents, extract text from them (using OCR if necessary), count embedded images, and ask questions based on the PDF content using a Groq LLM API.

## Features
Upload and process multiple PDF files

Extract text using PyPDF2

OCR support using Tesseract and Poppler for scanned or image-based PDFs

Automatically counts and reports the number of images in each PDF

Chat-style interface for querying PDF contents

Custom bubble-style buttons and dark/light theme support

Integration with Groq LLM API (e.g., llama3-8b-8192)

## Requirements
Python 3.8+

Streamlit

PyPDF2

pdf2image

pytesseract

PIL (Pillow)

requests

Poppler (installed and configured)

Tesseract OCR (installed and configured)

## Setup Instructions
Clone the Repository
Clone this project to your local system or run in a Streamlit environment like Kiro, Cursor, or your IDE.

## Install Required Packages

bash
Copy
Edit
pip install -r requirements.txt
### Install Tesseract OCR

Download and install from: https://github.com/tesseract-ocr/tesseract

Configure path in the code:

python
Copy
Edit
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
### Install Poppler

Download from: https://github.com/oschwartz10612/poppler-windows/releases/

## Configure path:

python
Copy
Edit
POPPLER_PATH = r"C:\path\to\poppler\bin"
Groq API Key
You can either:

Add it in secrets.toml:

toml
Copy
Edit
GROQ_API = "your_groq_api_key"
Or enter it manually in the sidebar input field.

Run the App

bash
Copy
Edit
streamlit run app.py
## How It Works
Upload one or more PDFs using the sidebar.

The app attempts to extract readable text using PyPDF2.

If no text is found (e.g., in scanned PDFs), it applies OCR using pytesseract and pdf2image.

It also counts the number of embedded images in each PDF and notifies the user.

Users can enter questions in a chat input field, and the app responds using Groq API.

## Image Support
The app counts and reports the number of images embedded in each PDF.

For better understanding of image content, integration with Vision-Language Models (VLMs) like those from vlm.run is recommended.

## Credits
Developed by Abhishek using Streamlit and Groq APIs. Designed to assist in PDF summarization, image detection, and AI-powered question answering.
