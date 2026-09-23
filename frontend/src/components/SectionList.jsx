export default function SectionList({title,items}) {
  return <section className="summary-section"><h3>{title}</h3>{items?.length?<ul>{items.map((x,i)=><li key={i}>{x}</li>)}</ul>:<p className="muted">Not clearly stated in the document.</p>}</section>
}
