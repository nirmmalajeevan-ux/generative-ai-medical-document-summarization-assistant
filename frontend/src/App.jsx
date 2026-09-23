import {useState} from "react";
import PatientCard from "./components/PatientCard";
import SummaryView from "./components/SummaryView";
import {summarizePdf,summarizeText} from "./services/api";

const sample=`Patient Name: John Doe
Date of Birth: MM/DD/YYYY
Date of Examination: MM/DD/YYYY
Physician: Dr. Jane Smith, MD
Specialty: General Medicine

Presenting Symptoms:
Persistent cough, wheezing, shortness of breath, and fatigue.

Diagnostic Tests Conducted:
Chest X-Ray: No signs of pneumonia.
Pulmonary Function Test: Decreased lung capacity.
Blood Tests: CBC showed elevated white blood cells.

Diagnosis:
Acute bronchitis superimposed on chronic asthma.

Medication:
Antibiotic course prescribed.
Corticosteroid inhaler prescribed.
Bronchodilators prescribed.

Treatment Plan:
Rest was recommended.
Avoid respiratory irritants.
Continue prescribed treatment.

Follow-up:
Reassessment scheduled in [NumberOfWeeks] weeks.`;

export default function App(){
 const[text,setText]=useState(""); const[file,setFile]=useState(null); const[result,setResult]=useState(null); const[error,setError]=useState(""); const[loading,setLoading]=useState(false); const[showSource,setShowSource]=useState(false);
 async function onText(e){e.preventDefault();setError("");setResult(null);if(text.trim().length<20){setError("Please enter a longer medical document.");return}setLoading(true);try{setResult(await summarizeText(text))}catch(err){setError(err.message)}finally{setLoading(false)}}
 async function onPdf(e){e.preventDefault();setError("");setResult(null);if(!file){setError("Choose a PDF first.");return}setLoading(true);try{setResult(await summarizePdf(file))}catch(err){setError(err.message)}finally{setLoading(false)}}
 return <main className="page">
  <header className="hero"><p className="eyebrow">GENERATIVE AI • MEDICAL NLP • V2</p><h1>Medical Document Summarization Assistant</h1><p>Cleaner extraction, structured summaries, duplicate removal, and safer output.</p></header>
  <div className="notice"><strong>Educational use only.</strong> This summarizes source text and does not diagnose or replace a clinician.</div>
  <div className="input-grid">
   <section className="panel"><h2>Paste Medical Text</h2><form onSubmit={onText}><textarea value={text} onChange={e=>setText(e.target.value)} placeholder="Paste medical report..."/><div className="actions"><button type="button" className="secondary" onClick={()=>setText(sample)}>Load Sample</button><button disabled={loading}>{loading?"Processing...":"Summarize Text"}</button></div></form></section>
   <section className="panel"><h2>Upload PDF</h2><form onSubmit={onPdf}><label className="file-box"><input type="file" accept=".pdf,application/pdf" onChange={e=>setFile(e.target.files?.[0]||null)}/><span>{file?file.name:"Choose a PDF document"}</span></label><p className="muted">Text-based PDFs supported. Scanned PDFs need OCR.</p><button disabled={loading}>{loading?"Processing...":"Summarize PDF"}</button></form></section>
  </div>
  {error&&<div className="error">{error}</div>}
  {result&&<section className="results"><PatientCard info={result.patient_info}/><div className="results-title"><h2>Generated Summary</h2><button className="secondary small" onClick={()=>setShowSource(v=>!v)}>{showSource?"Hide Source Preview":"Show Source Preview"}</button></div>{showSource&&<div className="source-preview"><h3>Cleaned Source Preview</h3><pre>{result.source_preview}</pre></div>}<SummaryView result={result}/><div className="warning-card"><h3>Verification Warnings</h3><ul>{result.warnings.map((x,i)=><li key={i}>{x}</li>)}</ul></div></section>}
 </main>
}
