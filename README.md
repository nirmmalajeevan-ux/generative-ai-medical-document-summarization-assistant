# Generative AI Medical Document Summarization Assistant V2

This version fixes malformed PDF text, repeated content, weak section detection, and unstructured output.

## Run backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Run frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

Start with `SUMMARIZER_MODE=fallback`. For optional generation, change `.env` to:

```env
SUMMARIZER_MODE=huggingface
HF_MODEL=google/flan-t5-base
```

The app is educational only and generated summaries must be checked against the original source.
