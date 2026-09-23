from app.text_cleaner import normalize_medical_text
from app.section_parser import parse_sections
from app.summarizer import fallback_summary

def test_labels():
    x=normalize_medical_text("PatientName:JohnDoe DateofBirth:MM/DD/YYYY Diagnosis:AcuteBronchitis")
    assert "Patient Name:" in x and "Date of Birth:" in x

def test_sections():
    x="Diagnosis:\nAcute bronchitis.\n\nMedication:\nCorticosteroid inhaler."
    s=parse_sections(x)
    assert any("bronchitis" in y.lower() for y in s["diagnoses"])
    assert any("inhaler" in y.lower() for y in s["medications"])

def test_summary():
    x="Presenting Symptoms:\nPersistent cough.\nDiagnosis:\nAcute bronchitis.\nTests and Results:\nChest X-Ray: No pneumonia."
    s=fallback_summary(x)
    assert "Acute bronchitis" in s.plain_language_summary
