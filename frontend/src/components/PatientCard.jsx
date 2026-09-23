export default function PatientCard({info}) {
  const rows=[["Patient",info.patient_name],["Date of Birth",info.date_of_birth],["Examination Date",info.date_of_examination],["Physician",info.physician],["Specialty",info.specialty]].filter(([,v])=>v);
  if(!rows.length)return null;
  return <section className="patient-card"><h2>Document Information</h2><div className="patient-grid">{rows.map(([l,v])=><div key={l}><span>{l}</span><strong>{v}</strong></div>)}</div></section>
}
