// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

// Function based component, represents the dialog which is shown to
// the user, after the user presses the download button, and some
// error has ocurred during the export process
function ErrorDialog(props) {
  return (
    <div className="med-export-dialog med-dialog">
      <i className="bx bxs-error" />
      <h1>An Error Occurred</h1>
      <div className="med-error-message">
        <span>
          An internal error occured during the exporting of the selected
          datapoints, please contact the administrator for more information.
        </span>
      </div>
      <button className="med-cancel-button" onClick={props.onClick}>
        Done
      </button>
    </div>
  )
}

export default ErrorDialog
