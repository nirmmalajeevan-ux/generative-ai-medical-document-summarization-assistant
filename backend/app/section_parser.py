import re

SECTION_MAP = {
"introduction":"clinical_context","clinical context":"clinical_context","medical history":"clinical_context",
"chief complaint":"symptoms","presenting symptoms":"symptoms","symptoms":"symptoms",
"history of present illness":"symptoms","hpi":"symptoms",
"diagnosis":"diagnoses","diagnoses":"diagnoses","assessment":"diagnoses","impression":"diagnoses",
"medication":"medications","medications":"medications",
"diagnostic tests conducted":"tests_and_results","tests and results":"tests_and_results",
"tests":"tests_and_results","investigations":"tests_and_results","laboratory":"tests_and_results","imaging":"tests_and_results",
"treatment plan":"treatment_plan","plan":"treatment_plan","treatment":"treatment_plan",
"recommendation":"treatment_plan","recommendations":"treatment_plan",
"follow-up":"follow_up","follow up":"follow_up","conclusion":"clinical_context"
}
PATIENT = {"patient name":"patient_name","date of birth":"date_of_birth",
"date of examination":"date_of_examination","physician":"physician","specialty":"specialty"}

def norm(x): return re.sub(r"\s+"," ",x.strip().rstrip(":")).lower()

def extract_patient_info(text):
    out={v:"" for v in PATIENT.values()}
    for line in text.splitlines():
        if ":" not in line: continue
        left,right=line.split(":",1); key=norm(left)
        if key in PATIENT and not out[PATIENT[key]]:
            val=right.strip()
            if len(val)<=120: out[PATIENT[key]]=val
    return out

def parse_sections(text):
    out={k:[] for k in ["clinical_context","symptoms","diagnoses","medications","tests_and_results","treatment_plan","follow_up"]}
    current=None
    for raw in text.splitlines():
        line=raw.strip()
        if not line: continue
        if ":" in line:
            left,right=line.split(":",1); h=norm(left)
            if h in PATIENT: continue
            if h in SECTION_MAP:
                current=SECTION_MAP[h]
                if right.strip(): out[current].append(right.strip())
                continue
        h=norm(line)
        if h in SECTION_MAP:
            current=SECTION_MAP[h]; continue
        if current: out[current].append(line)
    return out
