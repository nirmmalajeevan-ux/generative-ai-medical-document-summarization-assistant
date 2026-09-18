from pathlib import Path

import pandas as pd
import streamlit as st

from summarizer import DEFAULT_MODEL, summarize_medical_document

st.set_page_config(
    page_title="Medical Document Summarization Assistant",
    page_icon="🩺",
    layout="wide",
)

st.title("🩺 Generative AI-Based Medical Document Summarization Assistant")
st.caption("Educational demonstration only — not for diagnosis or treatment decisions.")

with st.sidebar:
    st.header("Model")
    st.code(DEFAULT_MODEL)
    st.info(
        "The first run downloads the model from Hugging Face and can take a few minutes."
    )

sample_path = Path("data/sample_clinical_notes.csv")
samples = pd.read_csv(sample_path) if sample_path.exists() else pd.DataFrame()

sample_text = ""
if not samples.empty:
    sample_name = st.selectbox(
        "Try a synthetic sample",
        ["Enter my own text"] + samples["title"].tolist(),
    )
    if sample_name != "Enter my own text":
        sample_text = samples.loc[samples["title"] == sample_name, "note"].iloc[0]

text = st.text_area(
    "Medical document",
    value=sample_text,
    height=330,
    placeholder="Paste a clinical note here...",
)

col1, col2 = st.columns([1, 4])
with col1:
    generate = st.button("Generate Summary", type="primary", use_container_width=True)

if generate:
    if len(text.strip()) < 20:
        st.warning("Please enter a longer clinical document.")
    else:
        with st.spinner("Generating summary..."):
            try:
                summary = summarize_medical_document(text)
                st.subheader("Generated Summary")
                st.write(summary)
            except Exception as exc:
                st.error(
                    "The model could not run. Check your internet connection and "
                    "installed dependencies."
                )
                st.exception(exc)

st.divider()
st.markdown(
    "**Privacy note:** Use synthetic or properly de-identified data for demonstrations. "
    "Do not paste identifiable patient information into an environment that is not "
    "approved for handling it."
)
