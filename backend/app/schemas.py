from typing import List
from pydantic import BaseModel, Field

class TextSummarizeRequest(BaseModel):
    text: str = Field(..., min_length=20, max_length=150000)

class PatientInfo(BaseModel):
    patient_name: str = ""
    date_of_birth: str = ""
    date_of_examination: str = ""
    physician: str = ""
    specialty: str = ""

class ClinicalSummary(BaseModel):
    clinical_context: str = ""
    symptoms: List[str] = []
    diagnoses: List[str] = []
    medications: List[str] = []
    tests_and_results: List[str] = []
    treatment_plan: List[str] = []
    follow_up: List[str] = []
    important_dates: List[str] = []
    plain_language_summary: str = ""
    red_flags: List[str] = []

class SummarizeResponse(BaseModel):
    patient_info: PatientInfo
    summary: ClinicalSummary
    model_mode: str
    redaction_applied: bool
    source_preview: str
    warnings: List[str]
