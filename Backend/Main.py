from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from OCR_ENGINE import perform_ocr

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

@app.get("/languages/")
def get_languages():
    return {
    "eng": "English",
    "ben": "Bengali",
    "guj": "Gujarati",
    "hin": "Hindi",
    "kan": "Kannada",
    "mal": "Malayalam",
    "pan": "Punjabi",
    "tam": "Tamil",
    "tel": "Telugu"
}

@app.post("/OCR")
async def ocr_image(file: UploadFile = File(...), lang: str = Form(...)):
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        text = perform_ocr(file_path, lang=lang)
        return JSONResponse(content={"text" : text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)