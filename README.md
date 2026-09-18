# Generative AI-Based Medical Document Summarization Assistant

A student project that demonstrates how generative AI can convert long clinical text into a concise, structured summary.

> **Educational use only.** This project is not a medical device and must not be used for diagnosis, treatment decisions, or emergency care.

## Features

- Paste a medical/clinical note into a Streamlit web app
- Generate a short structured summary
- Extract key sections such as conditions, medications, tests, and follow-up
- Load sample synthetic clinical notes for demonstration
- Uses an open-source Hugging Face model
- Includes links to public/synthetic datasets suitable for academic experimentation

## Project Structure

```text
.
├── app.py
├── summarizer.py
├── requirements.txt
├── DATASET.md
├── LICENSE
├── .gitignore
└── data/
    └── sample_clinical_notes.csv
```

## Dataset

For a shareable academic dataset, this project recommends the **Microsoft Clinical Visit Note Summarization Corpus**, which contains synthetic clinical encounters, dialogue transcripts, notes, and metadata and is distributed under CC BY 4.0.

Dataset repository:
https://github.com/microsoft/clinical_visit_note_summarization_corpus

The repository contains the MTS-Dialog and ACI-Bench collections.

For research with real de-identified ICU notes, MIMIC-III is another common option, but access requires credentialing and completion of the PhysioNet data-use requirements:
https://physionet.org/content/mimiciii/1.4/

See [DATASET.md](DATASET.md) for details.

## Installation

Clone the repository:

```bash
git clone https://github.com/nirmmalajeevan-ux/generative-ai-medical-document-summarization-assistant.git
cd generative-ai-medical-document-summarization-assistant
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit.

## How It Works

1. The user enters a clinical note.
2. The text is cleaned and length-limited for the model.
3. A prompt asks the language model to produce a concise medical-document summary.
4. The generated result is displayed in the web interface.

Default model: `google/flan-t5-small`.

You can change the model through the `MODEL_NAME` environment variable:

```bash
MODEL_NAME=google/flan-t5-base streamlit run app.py
```

## Example Input

```text
A 54-year-old patient presented with fever, productive cough and shortness
of breath for three days. Chest X-ray showed a right lower-lobe infiltrate.
The patient was treated with antibiotics and improved clinically.
```

## Example Output

```text
The patient presented with fever, productive cough and shortness of breath.
Imaging showed a right lower-lobe infiltrate consistent with pneumonia.
Antibiotic treatment was given and the patient improved.
```

## Technologies

Python, Streamlit, Hugging Face Transformers, PyTorch, Pandas and SentencePiece.

## Limitations

Generated summaries can omit details or produce incorrect statements. Results should always be checked against the source document. Do not upload identifiable patient data to systems unless you have the legal authority and appropriate privacy safeguards.

## License

MIT License for the code in this repository. Dataset licenses remain governed by their original publishers.
