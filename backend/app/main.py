from fastapi import FastAPI, UploadFile, File
from typing import Union
from pathlib import Path
import shutil
from fastapi import Query
from resume import PDFSummarizer

pdf_summarizer = PDFSummarizer()

app = FastAPI()

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):

    UPLOAD_DIR = Path("../uploaded_pdfs")
    UPLOAD_DIR.mkdir(exist_ok=True)

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "message": "Fichier reçu avec succès"}


@app.get("/resume")
async def resume_pdf(filename: str = Query(...)):
    UPLOAD_DIR = Path("../uploaded_pdfs")
    file_path = UPLOAD_DIR / filename.filename
    
    if not file_path.exists():
        return{"error": "fichier non trouver"}
    
    summary = await pdf_summarizer.summarize_pdf(file_path)
    return {"resume ", summary['output_text']}