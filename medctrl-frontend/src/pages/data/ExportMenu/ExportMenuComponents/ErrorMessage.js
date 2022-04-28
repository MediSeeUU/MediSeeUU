// function based element, represents an error message,
// to be displayed inside the export dialog
function ErrorMessage(props) {
  return (
    <div className="error med-error-message">
      <span className="error-header">An Error Occurred</span>
      <br />
      <span>{props.message}</span>
    </div>
  )
}

export default ErrorMessage
