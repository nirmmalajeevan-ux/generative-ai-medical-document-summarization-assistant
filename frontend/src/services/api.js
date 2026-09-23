const API_BASE="http://localhost:8000";
async function parseResponse(r){if(!r.ok){let m="Request failed.";try{const d=await r.json();m=d.detail||m}catch{}throw new Error(m)}return r.json()}
export async function summarizeText(text){return parseResponse(await fetch(`${API_BASE}/api/summarize/text`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text})}))}
export async function summarizePdf(file){const f=new FormData();f.append("file",file);return parseResponse(await fetch(`${API_BASE}/api/summarize/pdf`,{method:"POST",body:f}))}
