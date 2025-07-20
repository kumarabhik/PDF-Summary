# Updated PDF Summarizer Chatbot App (No Plagiarism, Fresh Theme)

import streamlit as st
import PyPDF2
from io import BytesIO
from pdf2image import convert_from_bytes
import pytesseract
from PIL import Image
import requests
import os

# OCR tool path (Tesseract)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = r"C:\Users\kumar\Downloads\XOXO\PDF Summarizer\Release-24.08.0-0\poppler-24.08.0\Library\bin"

# --- App Config & Styling ---
st.set_page_config("Vision-Powered PDF Assistant", layout="wide")
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
        }
        .stButton button {
            border-radius: 20px;
            padding: 10px 20px;
            background-color: #005f73;
            color: white;
            border: none;
            font-weight: bold;
            transition: 0.2s;
        }
        .stButton button:hover {
            background-color: #0a9396;
        }
        .reportview-container .main .block-container {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- OCR Extraction ---
def extract_text_with_ocr(pdf_bytes):
    images = convert_from_bytes(pdf_bytes, poppler_path=POPPLER_PATH)
    text_content = ""
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        text_content += f"\n\n[Page {i+1}]\n{text}"
    return text_content

# --- Text Extraction ---
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    return "".join([page.extract_text() for page in reader.pages if page.extract_text()])

# --- Validate PDF ---
def validate_pdf(file):
    try:
        if not file.name.endswith(".pdf"):
            return False
        file.seek(0)
        reader = PyPDF2.PdfReader(BytesIO(file.read()))
        return len(reader.pages) > 0
    except:
        return False

# --- Count Images ---
def count_images_in_pdf(file):
    file.seek(0)
    reader = PyPDF2.PdfReader(file)
    count = 0
    for page in reader.pages:
        try:
            xObj = page['/Resources']['/XObject'].get_object()
            for obj in xObj:
                if xObj[obj]['/Subtype'] == '/Image':
                    count += 1
        except:
            continue
    return count

# --- Sidebar Setup ---
st.sidebar.header("📄 Upload & Configure")
api_key = st.sidebar.text_input("🔑 Groq API Key", type="password")
st.session_state['GROQ_API'] = api_key
uploaded_files = st.sidebar.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)
clear = st.sidebar.button("🔁 Clear History")

if clear:
    st.session_state.messages = []

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome! Upload your PDF(s) to get started."}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- PDF Processing ---
pdf_text = ""
if uploaded_files:
    for file in uploaded_files:
        if validate_pdf(file):
            with st.spinner(f"📖 Reading {file.name}..."):
                text = extract_text_from_pdf(file)
                if not text:
                    st.warning(f"No text in {file.name}, applying OCR...")
                    file.seek(0)
                    text = extract_text_with_ocr(file.read())
                img_count = count_images_in_pdf(file)
                if img_count:
                    st.info(f"📷 {file.name} contains {img_count} image(s). VLMs are recommended for visual understanding.")
                pdf_text += text + "\n"
        else:
            st.warning(f"❌ {file.name} is not a valid PDF.")

# --- Question Answering ---
def query_groq(text, question):
    headers = {
        "Authorization": f"Bearer {st.session_state['GROQ_API']}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            *st.session_state.messages,
            {"role": "user", "content": f"Here is the context:\n{text[:5000]}\n\nNow answer this:\n{question}"}
        ],
        "temperature": 0.2,
        "max_tokens": 2000
    }
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
    else:
        raise RuntimeError(f"API Error: {res.status_code} - {res.text}")

if pdf_text:
    question = st.text_input("💬 Ask a question about the PDFs:")
    if question:
        with st.spinner("🤖 Thinking..."):
            try:
                answer = query_groq(pdf_text, question)
                with st.chat_message("assistant"):
                    st.markdown(answer)
                st.session_state.messages.append({"role": "user", "content": question})
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(str(e))
