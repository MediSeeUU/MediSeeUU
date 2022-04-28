// function based component, it represents a single procedure detail, which
// is used by the procedure component to display all the relevant information
function ProcedureDetail(props) {
  return (
    <div className={'procedure-detail ' + props.width}>
      <span className="procedure-label">{props.name}</span> <br />
      <span>{props.value}</span>
    </div>
  )
}

export default ProcedureDetail
