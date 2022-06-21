// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

// Function based component, it represents a single procedure detail, which
// is used by the procedure component to display all the relevant information
function ProcedureDetail(props) {
  return (
    <div className={'med-info-procedure-detail ' + props.width}>
      <span className="med-info-procedure-detail-label">{props.name}</span>{' '}
      <br />
      <span className="med-info-procedure-detail-value">{props.value}</span>
    </div>
  )
}

export default ProcedureDetail
