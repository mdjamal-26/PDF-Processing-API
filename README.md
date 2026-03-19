# PDF PROCESSING API

Upload a PDF resume and get structured JSON back — name, email, phone, and skills.

---

## Project Structure

```
resume_api/
├── app/
│   ├── main.py              # FastAPI app setup
│   ├── routes/
│   │   └── resume.py        # API endpoints
│   ├── services/
│   │   └── parser.py        # PDF reading + data extraction logic
│   └── schemas/
│       └── resume.py        # Pydantic response models
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
uvicorn app.main:app --reload
```

Server runs at: **http://localhost:8000**
Interactive docs at: **http://localhost:8000/docs**

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/upload-resume` | Upload PDF and parse it |
| GET | `/candidates` | List all parsed resumes (placeholder) |

---

## Sample Request

```bash
curl -X POST "http://localhost:8000/upload-resume" \
     -F "file=@resume.pdf"
```

## Sample Response

```json
{
  "success": true,
  "message": "Resume parsed successfully.",
  "data": {
    "filename": "john_resume.pdf",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+91-9876543210",
    "skills": ["python", "sql", "git", "docker"]
  }
}
```

## Error Responses

```json
{ "detail": "Only PDF files are accepted." }
{ "detail": "Uploaded file is empty." }
{ "detail": "Could not read the PDF. Make sure it is not corrupted." }
{ "detail": "No text found in PDF. It might be a scanned image." }
```
