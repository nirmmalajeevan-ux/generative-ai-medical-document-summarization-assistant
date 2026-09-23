def chunk_text(text, chunk_size=7000):
    if len(text)<=chunk_size: return [text]
    paras=[p.strip() for p in text.split("\n\n") if p.strip()]
    chunks=[]; current=""
    for p in paras:
        cand=(current+"\n\n"+p).strip()
        if len(cand)<=chunk_size:
            current=cand
        else:
            if current: chunks.append(current)
            if len(p)<=chunk_size: current=p
            else:
                for i in range(0,len(p),chunk_size): chunks.append(p[i:i+chunk_size])
                current=""
    if current: chunks.append(current)
    return chunks
