// function based component, represents the dialog which is shown to
// the user, after the user presses the download button, and some
// error has ocurred during the export process
function ErrorDialog(props) {
  return (
    <div className="export-dialog">
      <i className="bx bxs-error" />
      <h1>An Error Occurred</h1>
      <div className="error">
        <span>
          An internal error occured during the exporting of the selected
          datapoints, please contact the administrator for more information.
        </span>
      </div>
      <button className="cancel" onClick={props.onClick}>
        Done
      </button>
    </div>
  )
}

export default ErrorDialog
