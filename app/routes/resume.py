from fastapi import APIRouter, File, UploadFile, HTTPException
from app.schemas.resume import ResumeResponse
from app.services.parser import parse_resume

router = APIRouter()


@router.post("/upload-resume", response_model=ResumeResponse)
async def upload_resume(file: UploadFile = File(...)):

    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # Read bytes
    file_bytes = await file.read()

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # Parse the resume
    try:
        data = parse_resume(file_bytes, file.filename)
    except Exception:
        raise HTTPException(status_code=500, detail="Could not read the PDF. Make sure it is not corrupted.")

    if not data["name"] and not data["email"]:
        raise HTTPException(status_code=400, detail="No text found in PDF. It might be a scanned image.")

    return ResumeResponse(
        success=True,
        message="Resume parsed successfully.",
        data=data,
    )


@router.get("/candidates")
def get_candidates():
    # Placeholder — connect a database here to return stored results
    return {"message": "No database connected yet. This endpoint will list all parsed resumes."}
