from io import BytesIO
from pypdf import PdfReader

def extract_text_from_pdf(data: bytes) -> str:
    reader = PdfReader(BytesIO(data))
    pages=[]
    for i,page in enumerate(reader.pages,1):
        text = page.extract_text(extraction_mode="layout") or ""
        if text.strip():
            pages.append(f"\n--- PAGE {i} ---\n{text.strip()}")
    return "\n".join(pages)
