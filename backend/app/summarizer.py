import json, os, re
from functools import lru_cache
from .schemas import ClinicalSummary
from .section_parser import parse_sections
from .extractors import split_items,dedupe,extract_dates,fallback_keyword_extract,sentence_split
from .chunker import chunk_text

MODE=os.getenv("SUMMARIZER_MODE","fallback").lower()
HF_MODEL=os.getenv("HF_MODEL","google/flan-t5-base")
MAX_INPUT_CHARS=int(os.getenv("MAX_INPUT_CHARS","50000"))
CHUNK_SIZE=int(os.getenv("CHUNK_SIZE","7000"))

def fallback_summary(text):
    s=parse_sections(text)
    symptoms=dedupe(split_items(s["symptoms"]),8)
    diagnoses=dedupe(split_items(s["diagnoses"]),8)
    meds=dedupe(split_items(s["medications"]),8)
    tests=dedupe(split_items(s["tests_and_results"]),10)
    treatment=dedupe(split_items(s["treatment_plan"]),8)
    follow=dedupe(split_items(s["follow_up"]),6)

    if not symptoms:
        symptoms=fallback_keyword_extract(text,["fever","cough","fatigue","pain","wheezing","shortness of breath","headache","nausea","vomiting","dizziness"],6)
    if not diagnoses:
        diagnoses=fallback_keyword_extract(text,["diagnosis","diagnosed","assessment","impression","consistent with"],4)
    if not meds:
        meds=fallback_keyword_extract(text,["prescribed","medication","tablet","capsule","inhaler","antibiotic","bronchodilator","corticosteroid"," mg "],6)
    if not tests:
        tests=fallback_keyword_extract(text,["x-ray","xray","cbc","blood test","pulmonary function","mri","ct scan","ultrasound","laboratory"],8)
    if not treatment:
        treatment=fallback_keyword_extract(text,["treatment","plan","recommended","rest","hydration","continue","avoid exposure","medical leave"],6)
    if not follow:
        follow=fallback_keyword_extract(text,["follow-up","follow up","review","reassess","return"],4)

    context_items=dedupe(split_items(s["clinical_context"]),4)
    context=" ".join(context_items)[:1600]
    if not context:
        context=" ".join(sentence_split(text)[:4])[:1600]

    parts=[]
    if diagnoses: parts.append("The document mentions " + "; ".join(diagnoses[:2]) + ".")
    if symptoms: parts.append("Reported symptoms include " + "; ".join(symptoms[:3]) + ".")
    if tests: parts.append("Key investigations include " + "; ".join(tests[:3]) + ".")
    if treatment: parts.append("The plan includes " + "; ".join(treatment[:3]) + ".")
    if follow: parts.append("Follow-up information includes " + "; ".join(follow[:2]) + ".")
    plain=" ".join(parts)[:2200] or context

    red_flags=fallback_keyword_extract(text,["seek urgent","emergency","difficulty breathing","chest pain","confusion","worsening","persistent high fever"],5)

    return ClinicalSummary(
        clinical_context=context,
        symptoms=symptoms,
        diagnoses=diagnoses,
        medications=meds,
        tests_and_results=tests,
        treatment_plan=treatment,
        follow_up=follow,
        important_dates=extract_dates(text),
        plain_language_summary=plain,
        red_flags=red_flags,
    )

@lru_cache(maxsize=1)
def _pipeline():
    from transformers import pipeline
    return pipeline("text2text-generation",model=HF_MODEL)

def _generate_json(chunk):
    prompt = """You summarize medical documents.
Use only facts explicitly stated in the source.
Do not diagnose, infer, or invent missing values.
Preserve placeholders such as [NumberOfWeeks].
Keep list items short and factual.
Return VALID JSON only, no markdown, using exactly these keys:
clinical_context, symptoms, diagnoses, medications, tests_and_results,
treatment_plan, follow_up, important_dates, plain_language_summary, red_flags.
List-valued keys must contain JSON arrays.

SOURCE:
""" + chunk
    raw=_pipeline()(prompt,max_new_tokens=900,do_sample=False,truncation=True)[0]["generated_text"]
    m=re.search(r"\{.*\}",raw,flags=re.S)
    return json.loads(m.group(0) if m else raw)

def _merge(parts,source):
    fb=fallback_summary(source)
    list_keys=["symptoms","diagnoses","medications","tests_and_results","treatment_plan","follow_up","important_dates","red_flags"]
    acc={k:[] for k in list_keys}
    contexts=[]; plains=[]
    for part in parts:
        if part.get("clinical_context"): contexts.append(str(part["clinical_context"]))
        if part.get("plain_language_summary"): plains.append(str(part["plain_language_summary"]))
        for k in list_keys:
            v=part.get(k,[])
            if isinstance(v,list): acc[k].extend(str(x) for x in v if str(x).strip())
    return ClinicalSummary(
        clinical_context=" ".join(dedupe(contexts,3))[:1800] or fb.clinical_context,
        symptoms=dedupe(acc["symptoms"],8) or fb.symptoms,
        diagnoses=dedupe(acc["diagnoses"],8) or fb.diagnoses,
        medications=dedupe(acc["medications"],8) or fb.medications,
        tests_and_results=dedupe(acc["tests_and_results"],10) or fb.tests_and_results,
        treatment_plan=dedupe(acc["treatment_plan"],8) or fb.treatment_plan,
        follow_up=dedupe(acc["follow_up"],6) or fb.follow_up,
        important_dates=dedupe(acc["important_dates"],10) or fb.important_dates,
        plain_language_summary=" ".join(dedupe(plains,3))[:2200] or fb.plain_language_summary,
        red_flags=dedupe(acc["red_flags"],6) or fb.red_flags,
    )

def summarize_medical_document(text):
    text=text[:MAX_INPUT_CHARS]
    if MODE!="huggingface":
        return fallback_summary(text),"fallback"
    try:
        parts=[_generate_json(c) for c in chunk_text(text,CHUNK_SIZE)]
        return _merge(parts,text),"huggingface"
    except Exception:
        return fallback_summary(text),"fallback-after-model-error"
