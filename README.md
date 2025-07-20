# PDF Summarizer Chatbot

This project is a **Streamlit-based web application** that allows users to upload multiple PDF files, extract text (including via OCR for scanned PDFs), count embedded images, and ask questions about the content using a **Groq LLM API**. It also optionally supports image reasoning using a **Vision-Language Model (VLM)** API like [vlm.run](https://app.vlm.run/).

---

## Features

- Upload and analyze multiple PDFs at once.
- Extract readable text directly or via **OCR** (Tesseract + Poppler).
- Detect and count images embedded in PDF pages.
- Ask questions about the PDFs via **Groq LLM API**.
- Supports theme customization and improved button styling.
- Optional: Use VLM.run API for PDFs with **heavy image content**.

---

## Setup Instructions

### 1. Install Requirements

Make sure you have Python 3.9+ installed.

```bash
pip install -r requirements.txt
```

You also need:

- **[Tesseract OCR](https://github.com/tesseract-ocr/tesseract)**
- **[Poppler for Windows](http://blog.alivate.com.au/poppler-windows/)**

Set their paths in your script:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Path\To\poppler-xx\Library\bin"
```

---

## How to Run

```bash
streamlit run your_script_name.py
```

---

## Required Secrets

Create a `secrets.toml` file (in `.streamlit/`) for your Groq API key:

```toml
GROQ_API = "your-groq-api-key"
```

If you're also using VLM.run for vision-related queries:

```toml
VLM_API = "your-vlm-run-api-key"
```

---

## Optional: Enable VLM.run for Image-Based Queries

To use [vlm.run](https://app.vlm.run/) for image-based understanding:

1. **Get your API key** from [https://app.vlm.run/dashboard](https://app.vlm.run/dashboard).
2. Add it to your `secrets.toml` as shown above.
3. Modify your Streamlit script to detect when image content is high and route queries to VLM.run.

Example addition:

```python
if img_count > 0:
    # Optional call to VLM.run if you want image reasoning
    vlm_headers = {
        "Authorization": f"Bearer {st.secrets['VLM_API']}",
        "Content-Type": "application/json"
    }
    vlm_payload = {
        "model": "vlm-v1",
        "prompt": "Summarize this image:",
        "image": encoded_image  # base64 or binary content
    }
    response = requests.post("https://api.vlm.run/v1/chat/completions", headers=vlm_headers, json=vlm_payload)
```

You’ll need to extract and encode the images using `pdf2image` or `PyMuPDF` to pass them as base64 to VLM.run.

---

## Credits

- Built using **Streamlit**, **Tesseract OCR**, and **Groq LLM APIs**.
- Image reasoning via **[VLM.run](https://app.vlm.run/)** (optional).
