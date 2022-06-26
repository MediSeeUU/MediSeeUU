// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useState } from 'react'
import handleLogin from '../handlers/login'
import ErrorMessage from '../../pages/data/selected_data/export_menu/components/ErrorMessage'

// Function based component rendering the login form
function LoginForm(props) {
  // State that keeps track whether the login has failed (by default false)
  const [fail, setFail] = useState(false)

  // Handler for closing the dialog
  const closeDialog = () => {
    props.onClose()
  }

  // Handler for logging in the user
  const connection = async (event) => {
    event.preventDefault()

    // Call the login handler
    const success = await handleLogin(event, props.state)

    // If login was successful, then set the username and access level in the navigation bar
    if (success) {
      let username = sessionStorage.getItem('username')
      let access_level = sessionStorage.getItem('access_level')

      props.parent.setState({
        loggedin: true,
        userName: username,
        accessLevel: access_level,
      })
    // If login failed, set fail state to true which renders the error message
    } else {
      setFail(true)
    }
  }

  // Render all the components of the login form
  return (
    <div className="med-dialog">
      <i className="bx bxs-log-in" />
      <h1>Login</h1>
      <span className="med-description">
        Please fill in your credentials. If you do not have an account yet and
        think you are entitled to one, please contact the administrator.
      </span>
      <form name="loginForm" onSubmit={connection}>
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
        {/* Render error message if fail state is true */}
        {fail && (
          <ErrorMessage
            message={
              'Wrong username or password. Please check your credentials and try again.'
            }
          />
        )}
        <button
          type="submit"
          className="med-button-login med-primary-solid med-bx-button"
        >
          Sign in
        </button>
        <button className="med-cancel-button" onClick={closeDialog}>
          Cancel
        </button>
      </form>
    </div>
  )
}

export default LoginForm
