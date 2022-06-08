// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
// function based component, represents the dialog which is shown to
// the user, after the user presses the save button, and the saving
// process has completed successfully
function SuccessDialog(props) {
  return (
    <div className="med-save-dialog">
      <i className="bx bx-check" />
      <h1>Selection Successfully Saved</h1>
      <div className="med-success-message">
        <span>
          Saving the selection of {props.num} data points has completed
          successfully.
        </span>
      </div>
      <button className="cancel" onClick={props.onClick}>
        Done
      </button>
    </div>
  )
}

export default SuccessDialog
