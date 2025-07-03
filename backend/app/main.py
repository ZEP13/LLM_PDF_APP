from fastapi import FastAPI, UploadFile, File
from typing import Union
from pathlib import Path
import shutil
from fastapi import Query
from resume import PDFSummarizer
from chat import Chat
from fastapi.middleware.cors import CORSMiddleware



pdf_summarizer = PDFSummarizer()
chatClass = Chat()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or set to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):

    UPLOAD_DIR = Path("../uploaded_pdfs")
    UPLOAD_DIR.mkdir(exist_ok=True)

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "message": "Fichier reçu avec succès"}


@app.get("/resume")
async def resume_pdf(level_prompt: int,filename: str = Query(...)):
    UPLOAD_DIR = Path("../uploaded_pdfs")
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        return{"error": "fichier non trouver"}
    
    summary = pdf_summarizer.summarize_pdf(file_path, level_prompt)
    return {"resume": summary['output_text']}




@app.post('/chat/')
async def chatia(message_user: str, filename: str = Query(...)):
    UPLOAD_DIR = Path("../uploaded_pdfs")
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        return{"error": "fichier non trouver"}
    
    chat = chatClass.setup_qa_systeme(file_path, message_user)

    return {"AI answer": chat['output_text']}
