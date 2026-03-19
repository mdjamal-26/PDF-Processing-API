from fastapi import FastAPI, UploadFile, File, HTTPException
import pdfplumber
import re
import io

app = FastAPI(title="Resume Parser API")


def extract_text_from_pdf(file_bytes):
    """Extract all text from PDF bytes."""
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_email(text):
   """Find email using regex."""
   match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
   return match.group(0) if match else None


def extract_phone(text):
    """Find phone number using regex."""
    match = re.search(r"(\+?\d[\d\s\-().]{7,}\d)", text)
    return match.group(0).strip() if match else None


def extract_name(text):
    """Get name from the first line of the resume."""
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if lines:
        return lines[0]
    return None


def extract_skills(text):
    """Match skills from a keyword list."""
    skills_list = [
        "python","java", "javascript", "c++", "sql", "html", "css",
        "react", "nodejs","django", "flask", "fastapi", "git", "docker",
        "machine learning","data analysis", "aws", "linux", "mongodb"
    ]

    text_lower = text.lower()
    found = [skill for skill in skills_list if skill in text_lower]

    return found


# ── Endpoints ─────────────────────────────────────────────

@app.get("/")
def home():
    return {"message": "Resume Parser API is running!", "upload_endpoint": "/upload-resume"}


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    # check file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # read file
    file_bytes = await file.read()

    if len(file_bytes)==0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # extract text
    try:
        text = extract_text_from_pdf(file_bytes)
    except Exception:
         raise HTTPException(status_code=500, detail="Could not read the PDF. Make sure it's not corrupted.")

    if not text.strip():
        raise HTTPException(status_code=400, detail="No text found in PDF. It might be a scanned image.")

    # parse fields
    result = {
        "filename": file.filename,
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }

    return {
        "success": True,
        "message": "Resume parsed successfully.",
        "data": result
    }