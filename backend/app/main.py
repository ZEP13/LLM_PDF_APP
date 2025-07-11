from fastapi import FastAPI, UploadFile, File
from typing import Union
from pathlib import Path
import shutil
from fastapi import Query
from resume import PDFSummarizer
from chat import Chat
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import FileResponse
from fastapi import HTTPException

pdf_summarizer = PDFSummarizer()


loaded_pdfs = {}
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("../uploaded_pdfs")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    chat_instance  = Chat()
    chat_instance.setup_qa_systeme(str(file_path))
    loaded_pdfs[file.filename] = chat_instance

    return {"filename": file.filename, "message": "Fichier reçu avec succès"}

@app.get("/get-pdf/{filename}")
async def get_pdf(filename: str):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Fichier non trouvé")
    return FileResponse(path=file_path, media_type="application/pdf")

@app.get("/resume")
async def resume_pdf(level_prompt: int,filename: str = Query(...)): #attend dans l'URL (query string)
    file_path = UPLOAD_DIR / filename
    
    if not file_path.exists():
        return{"error": "fichier non trouver"}
    
    summary = pdf_summarizer.summarize_pdf(file_path, level_prompt-1)
    return {"resume": summary['output_text']}


@app.post("/chat/")
async def chatia(question_user: str, filename: str = Query(...)):
    if filename not in loaded_pdfs:
        return {"error": f"Fichier '{filename}' non chargé. Upload d'abord le PDF."}

    try:
        chat_instance = loaded_pdfs[filename]
        response = chat_instance.chat(question_user)
        return {"AI_answer": response}
    except Exception as e:
        return {"error": str(e)}
