import os
from functools import lru_cache
from typing import Optional

from transformers import pipeline

DEFAULT_MODEL = os.getenv("MODEL_NAME", "google/flan-t5-small")


@lru_cache(maxsize=1)
def get_summarizer(model_name: str = DEFAULT_MODEL):
    """Load and cache the text2text generation pipeline."""
    return pipeline(
        "text2text-generation",
        model=model_name,
        tokenizer=model_name,
    )


def summarize_medical_document(
    text: str,
    model_name: str = DEFAULT_MODEL,
    max_new_tokens: int = 180,
) -> str:
    """Generate a concise educational summary of a clinical document."""
    cleaned = " ".join(text.split())
    if not cleaned:
        return ""

    # Small FLAN-T5 models have limited context, so keep the demo input bounded.
    cleaned = cleaned[:5000]

    prompt = (
        "Summarize the following clinical document accurately and concisely. "
        "Include the main complaint, important findings, diagnosis or assessment, "
        "treatment, and follow-up when present. Do not invent information.\n\n"
        f"Clinical document:\n{cleaned}\n\nSummary:"
    )

    generator = get_summarizer(model_name)
    result = generator(
        prompt,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        truncation=True,
    )
    return result[0]["generated_text"].strip()
