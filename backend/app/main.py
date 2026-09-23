from fastapi import FastAPI,File,HTTPException,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from .schemas import PatientInfo,SummarizeResponse,TextSummarizeRequest
from .pdf_utils import extract_text_from_pdf
from .text_cleaner import normalize_medical_text
from .section_parser import extract_patient_info
from .privacy import redact_common_identifiers
from .summarizer import summarize_medical_document

app=FastAPI(title="Medical Document Summarization Assistant V2",version="2.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

WARNINGS=[
"Generated summaries can omit or misstate information.",
"Verify important details against the original document.",
"This tool does not diagnose conditions or replace a qualified clinician."
]

@app.get("/")
def root(): return {"message":"Medical Document Summarization Assistant V2","docs":"/docs"}

@app.get("/health")
def health(): return {"status":"ok","version":"2.0.0"}

def process_text(raw):
    if len(raw.strip())<20: raise HTTPException(400,"Document text is too short.")
    normalized=normalize_medical_text(raw)
    patient=extract_patient_info(normalized)
    redacted,changed=redact_common_identifiers(normalized)
    summary,mode=summarize_medical_document(redacted)
    return SummarizeResponse(patient_info=PatientInfo(**patient),summary=summary,model_mode=mode,redaction_applied=changed,source_preview=normalized[:3500],warnings=WARNINGS)

@app.post("/api/summarize/text",response_model=SummarizeResponse)
def summarize_text(payload:TextSummarizeRequest): return process_text(payload.text)

@app.post("/api/summarize/pdf",response_model=SummarizeResponse)
async def summarize_pdf(file:UploadFile=File(...)):
    if file.content_type not in ("application/pdf","application/octet-stream"):
        raise HTTPException(400,"Please upload a PDF file.")
    data=await file.read()
    if len(data)>15*1024*1024: raise HTTPException(413,"PDF is larger than 15 MB.")
    try: text=extract_text_from_pdf(data)
    except Exception as e: raise HTTPException(400,f"Unable to read PDF: {e}")
    if not text.strip(): raise HTTPException(400,"No extractable text found. Scanned/image PDFs need OCR.")
    return process_text(text)
