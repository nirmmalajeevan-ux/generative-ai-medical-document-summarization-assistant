import re

LABELS = [
"Patient Name","Date of Birth","Date of Examination","Physician","Specialty",
"Contact Information","Introduction","Medical History","Presenting Symptoms",
"Chief Complaint","History of Present Illness","Diagnostic Tests Conducted",
"Tests and Results","Diagnosis","Assessment","Medications","Medication",
"Treatment Plan","Plan","Follow-up","Follow Up","Recommendation","Recommendations","Conclusion"
]

JOINED = {
"PatientName":"Patient Name","DateofBirth":"Date of Birth","DateofExamination":"Date of Examination",
"MedicalHistory":"Medical History","PresentingSymptoms":"Presenting Symptoms",
"DiagnosticTestsConducted":"Diagnostic Tests Conducted","TreatmentPlan":"Treatment Plan",
"ChestX-Ray":"Chest X-Ray","PulmonaryFunctionTest":"Pulmonary Function Test",
"BloodTests":"Blood Tests","GeneralMedicine":"General Medicine",
}

def normalize_medical_text(text: str) -> str:
    text=text.replace("\\r","\\n").replace("\\\\:",":")
    for old,new in JOINED.items():
        text=re.sub(re.escape(old),new,text,flags=re.I)

    # Put important labels on their own lines.
    for label in sorted(LABELS,key=len,reverse=True):
        compact=re.sub(r"\s+","",label)
        text=re.sub(re.escape(compact)+r"\s*:", label+":", text, flags=re.I)
        text=re.sub(rf"(?<!\n)\b{re.escape(label)}\s*:", "\n"+label+":", text, flags=re.I)

    # Add obvious missing spaces while avoiding damage to numbers.
    text=re.sub(r":(?=[A-Za-z\[])",
                ": ", text)
    text=re.sub(r"(?<=[a-z])(?=[A-Z])"," ",text)

    # Repair a set of frequent joined clinical expressions.
    replacements = {
        "shortnessofbreath":"shortness of breath",
        "whitebloodcells":"white blood cells",
        "nosignsoflunginfection":"no signs of lung infection",
        "decreasedlungcapacity":"decreased lung capacity",
        "acute bronchitissuperimposedonchronic asthma":"acute bronchitis superimposed on chronic asthma",
        "acutebronchitis":"acute bronchitis",
        "chronicasthma":"chronic asthma",
    }
    for old,new in replacements.items():
        text=re.sub(re.escape(old),new,text,flags=re.I)

    text=re.sub(r"--- PAGE \d+ ---","",text,flags=re.I)
    text=re.sub(r"[ \t\xa0]+"," ",text)
    text=re.sub(r" *\n *","\n",text)
    text=re.sub(r"\n{3,}","\n\n",text)
    text=re.sub(r"(?<!\n)\s+(\d+[.)])\s+",r"\n\1 ",text)
    return text.strip()
