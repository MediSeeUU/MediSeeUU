// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import ProcedureDetail from './ProcedureDetail'
import CustomLink from './CustomLink'

// Function based component, represents a single procedure and displays the
// following relevant information: the decision date and number, as well as the
// type of the procedure. There are also two links provided to both the annex
// and the decision file.
function Procedure(props) {
  const clean = (value) => {
    return !value ? 'NA' : value
  }

  let decisionDate = clean(props.proc.decisiondate)
  let procedureType = clean(props.proc.proceduretype)
  let decisionNumber = clean(props.proc.decisionnumber)

  let annexURL = props.proc.annexurl
  let decisionURL = props.proc.decisionurl

  return (
    <div className="med-info-procedure">
      <div className="med-info-procedure-content">
        <ProcedureDetail
          name="Decision Date"
          value={decisionDate}
          width="small-width"
        />
        <ProcedureDetail
          name="Procedure Type"
          value={procedureType}
          width="large-width"
        />
        <ProcedureDetail
          name="Decision Number"
          value={decisionNumber}
          width="small-width"
        />
      </div>

      <div className="med-info-procedure-file-link-container">
        <CustomLink
          className="med-info-procedure-file-link"
          name="Annex File"
          image="bx bx-file-blank"
          dest={annexURL}
        />

        <CustomLink
          className="med-info-procedure-file-link"
          name="Decision File"
          image="bx bx-file-blank"
          dest={decisionURL}
        />
      </div>
    </div>
  )
}

export default Procedure
