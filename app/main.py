from fastapi import FastAPI
from app.routes.resume import router

app = FastAPI(title="Resume Parser API")

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Resume Parser API is running!", "docs": "/docs"}



