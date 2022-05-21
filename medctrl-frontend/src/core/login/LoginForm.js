import React from 'react'
import handleLogin from './connectionServer'
import ErrorMessage from '../../pages/data/ExportMenu/ExportMenuComponents/ErrorMessage'

class LoginForm extends React.Component {
  // LoginForm is a class based component which renders the login form
  constructor(props) {
    super(props)
    this.state = {
      onClose: props.onClose,
      errorMessage: '',
    }

    this.errorWrongCredentials =
      'Wrong username or password. Please check your credentials and try again.'

    this.closeDialog = this.closeDialog.bind(this)
    this.connection = this.connection.bind(this)
  }

  // method used for the handling the closing of the dialog
  closeDialog() {
    this.state.onClose()
  }

  async connection(event) {
    event.preventDefault()
    var success = await handleLogin(event, this.props.state)

    if (success) {
      let username = sessionStorage.getItem('username')
      let access_level = sessionStorage.getItem('access_level')

      this.props.parent.setState({
        loggedin: true,
        userName: username,
        accessLevel: access_level,
      })
      return
    }

    this.setState({ errorMessage: this.errorWrongCredentials })
  }

  // render the login form
  render() {
    var errorMessage = null

    if (this.state.errorMessage !== '') {
      errorMessage = <ErrorMessage message={this.state.errorMessage} />
    }

    return (
      <div className="med-login-dialog">
        <i className="bx bxs-log-in" />
        <h1>Login</h1>
        <span className="med-description">
          Please fill in your credentials. If you do not have an account yet and
          think you are entitled to one, please contact the administrator.
        </span>
        <form name="loginForm" onSubmit={this.connection}>
          <input
            type="text"
            id="username"
            className="med-credential-input med-text-input"
            placeholder="Username"
            minLength={4}
            maxLength={64}
            autoComplete="off"
            spellCheck="false"
          />
          <input
            type="password"
            id="password"
            className="med-credential-input med-text-input"
            placeholder="Password"
          />
          {errorMessage}
          <button
            type="submit"
            className="med-button-login med-primary-solid med-bx-button"
          >
            Sign in
          </button>
          <button className="med-button-cancel" onClick={this.closeDialog}>
            Cancel
          </button>
        </form>
      </div>
    )
  }
}

export default LoginForm
