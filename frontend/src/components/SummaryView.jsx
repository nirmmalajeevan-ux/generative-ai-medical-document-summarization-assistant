import SectionList from "./SectionList";
export default function SummaryView({result}) {
  const s=result.summary;
  return <div className="summary-card">
    <div className="summary-meta"><span>Mode: {result.model_mode}</span><span>PII redaction: {result.redaction_applied?"Applied":"Not triggered"}</span></div>
    <section className="summary-section"><h3>Clinical Context</h3><p>{s.clinical_context||"Not clearly stated."}</p></section>
    <SectionList title="Symptoms / Complaints" items={s.symptoms}/>
    <SectionList title="Diagnoses Mentioned" items={s.diagnoses}/>
    <SectionList title="Medications Mentioned" items={s.medications}/>
    <SectionList title="Tests and Results" items={s.tests_and_results}/>
    <SectionList title="Treatment / Plan" items={s.treatment_plan}/>
    <SectionList title="Follow-up" items={s.follow_up}/>
    <SectionList title="Important Dates" items={s.important_dates}/>
    <SectionList title="Red Flags / Urgent Instructions" items={s.red_flags}/>
    <section className="summary-section plain-language"><h3>Plain-language Summary</h3><p>{s.plain_language_summary||"Not available."}</p></section>
  </div>
}
