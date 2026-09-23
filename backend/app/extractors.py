import re

def split_items(lines):
    out=[]
    for line in lines:
        line=re.sub(r"^\s*\d+[.)]\s*","",line).strip(" -•")
        if not line: continue
        parts=re.split(r"(?<=[.;])\s+(?=[A-Z])",line)
        out.extend([p.strip(" -•") for p in parts if p.strip(" -•")])
    return out

def dedupe(items,limit=10):
    result=[]; seen=[]
    for item in items:
        clean=re.sub(r"\s+"," ",item).strip(" -•")
        if len(clean)<3: continue
        norm=re.sub(r"[^a-z0-9 ]+","",clean.lower())
        words=set(norm.split())
        dup=False
        for pn,pw in seen:
            if norm==pn:
                dup=True; break
            if words and pw:
                overlap=len(words & pw)/max(1,min(len(words),len(pw)))
                if overlap>0.86:
                    dup=True; break
        if not dup:
            result.append(clean); seen.append((norm,words))
        if len(result)>=limit: break
    return result

def extract_dates(text):
    pats=[
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b",
        r"\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},?\s+\d{4}\b"
    ]
    found=[]
    for p in pats: found.extend(re.findall(p,text,flags=re.I))
    return list(dict.fromkeys(found))[:10]

def sentence_split(text):
    text=re.sub(r"\s+"," ",text).strip()
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+",text) if len(x.strip())>8]

def fallback_keyword_extract(text,keywords,limit=6):
    return dedupe([s for s in sentence_split(text) if any(k in s.lower() for k in keywords)],limit)
