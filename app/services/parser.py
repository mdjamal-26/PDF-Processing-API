import re
import io
import pdfplumber


SKILLS_LIST = [
    "python", "java", "javascript", "c++", "sql", "html", "css",
    "react", "nodejs", "django", "flask", "fastapi", "git", "docker",
    "machine learning", "data analysis", "aws", "linux", "mongodb"
]


def extract_text(file_bytes: bytes) -> str:
    """Extract all text from a PDF file."""
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_name(text: str):
    """Return the first non-empty line as the candidate's name."""
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return lines[0] if lines else None


def extract_email(text: str):
    """Find an email address using regex."""
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None


def extract_phone(text: str):
    """Find a phone number using regex."""
    match = re.search(r"(\+?\d[\d\s\-().]{7,}\d)", text)
    return match.group(0).strip() if match else None


def extract_skills(text: str):
    """Match skills against a predefined keyword list."""
    text_lower = text.lower()
    return [skill for skill in SKILLS_LIST if skill in text_lower]


def parse_resume(file_bytes: bytes, filename: str) -> dict:
    """Main function — extracts all fields and returns a dict."""
    text = extract_text(file_bytes)
    return {
        "filename": filename,
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
    }
