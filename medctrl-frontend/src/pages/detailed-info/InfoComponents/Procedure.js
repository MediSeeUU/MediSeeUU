import ProcedureDetail from './ProcedureDetail'
import CustomLink from './CustomLink'

// function based component, represents a single procedure and displays the
// following relevant information: the decision date and number, as well as the
// type of the procedure. there are also two links provided to both the annex
// and the decision file.
function Procedure(props) {
  let decisionDate = props.proc.DecisionDate
  let procedureType = props.proc.ProcType
  let decisionNumber = props.proc.DecisionNumber

  let annexURL = props.proc.AnnexURL
  let decisionURL = props.proc.DecisionURL

  return (
    <div class="procedure">
      <div class="procedure-content">
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

      <div class="procedure-files">
        <CustomLink
          className="procedure-file-link"
          name="Annex File"
          image="bx bx-file-blank"
          dest={annexURL}
        />

        <CustomLink
          className="procedure-file-link"
          name="Decision File"
          image="bx bx-file-blank"
          dest={decisionURL}
        />
      </div>
    </div>
  )
}

export default Procedure
