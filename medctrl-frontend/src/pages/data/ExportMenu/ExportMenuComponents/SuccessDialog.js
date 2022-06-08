// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
// function based component, represents the dialog which is shown to
// the user, after the user presses the download button, and the export
// has completed succesfully
function SuccessDialog(props) {
  return (
    <div className="med-export-dialog">
      <i className="bx bx-check" />
      <h1>Export Successfull</h1>
      <div className="med-success-message">
        <span>
          The export of all {props.num} selected data points has completed
          successfully. The download should start shortly. If the download does
          not start, please contact the administrator for more information.
        </span>
      </div>
      <button className="cancel" onClick={props.onClick}>
        Done
      </button>
    </div>
  )
}

export default SuccessDialog
