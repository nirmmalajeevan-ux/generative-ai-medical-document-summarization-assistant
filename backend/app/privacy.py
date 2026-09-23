import re

PATTERNS = [
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"), "[REDACTED_EMAIL]"),
    (re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b"), "[REDACTED_PHONE]"),
    (re.compile(r"\b\d{10,18}\b"), "[REDACTED_ID]"),
]

def redact_common_identifiers(text):
    out=text; changed=False
    for pat,repl in PATTERNS:
        new=pat.sub(repl,out)
        changed |= (new != out)
        out=new
    return out, changed
