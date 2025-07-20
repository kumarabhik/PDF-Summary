@echo off
echo ✅ Activating virtual environment...
call pdf_env\Scripts\activate

echo 🔄 Cleaning __pycache__ folders and .pyc files...
for /r %%i in (__pycache__) do (
    echo Deleting %%i
    rd /s /q "%%i"
)
for /r %%f in (*.pyc) do (
    echo Deleting %%f
    del "%%f"
)

echo 🚀 Launching PDF Summarizer App...
streamlit run PDF.py

pause
