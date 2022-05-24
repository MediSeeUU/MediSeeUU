// function based element, represents an error message,
// to be displayed inside the save dialog
function ErrorMessage(props) {
  return (
    <div className="med-error-message">
      <span className="med-error-message-header">An Error Occurred</span>
      <br />
      <span>{props.message}</span>
    </div>
  )
}

export default ErrorMessage
