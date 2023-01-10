// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import ErrorDialog from './components/ErrorDialog'
import SuccessDialog from './components/SuccessDialog'
import ErrorMessage from './components/ErrorMessage'
import postSavedSelection from './SaveHandler'

// Class based component which renders the save dialog.
// It is passed some series of data points, and it allows
// the user to save these points as a selection with a name.
// A class is used instead of a function because of the extensive state.
class SaveDialog extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      dialogState: 'default',
      saveName: '',
      onClose: props.onClose,
      errorMessage: '',
    }

    this.selectedData = props.data

    this.noSaveName =
      'No name for the selected data points has been entered. Please give a name to the selection to be able to distinguish saved selections.'
    this.invalidName =
      'The name entered is invalid. Selection names can only contain Latin characters, digits, dashes (-), underscores (_), and spaces.'

    this.closeDialog = this.closeDialog.bind(this)
    this.handleSave = this.handleSave.bind(this)
    this.handleChange = this.handleChange.bind(this)
  }

  // Handler to close the dialog
  closeDialog() {
    this.state.onClose()
  }

  // Method used for handling when the user presses the save button
  // first it is checked if the current dialog state is valid, if so the
  // data is saved, otherwise an error is displayed
  async handleSave(event) {
    event.preventDefault()

    // eunumbers of selected data points
    var eu_pnumbers = []
    this.selectedData.forEach((dataPoint) =>
      eu_pnumbers.push(dataPoint.eu_pnumber)
    )

    // Check whether the name field has actual input
    if (this.state.saveName === '') {
      this.setState({ errorMessage: this.noSaveName })
      return
    }

    // Check whether only allowed characters are used
    if (!/^[A-Za-z0-9\-_ ]*$/.test(this.state.saveName)) {
      this.setState({ errorMessage: this.invalidName })
      return
    }

    // Send the saved selections to the server
    const succes = await postSavedSelection(eu_pnumbers, this.state.saveName)

    // Update dialog state based on the status returned by the server
    if (succes) {
      this.setState({ dialogState: 'success' })
    } else {
      this.setState({ dialogState: 'error' })
    }
  }

  // When the user updates the input field in the dialog,
  // this method is used to update the current state of the dialog
  // to reflect this user interaction
  handleChange(event) {
    this.setState({ saveName: event.target.value })
  }

  // Depending on the state of the dialog, a specific dialog is rendered
  // if the user has given a valid name, the selection is saved
  // (success) or an error has occurred (error). If any error messages need
  // to be displayed in the default view these are added dynamically.
  render() {
    const dialogState = this.state.dialogState
    if (dialogState === 'success')
      return (
        <SuccessDialog
          num={this.selectedData.length}
          onClick={this.closeDialog}
        />
      )

    if (dialogState === 'error')
      return <ErrorDialog onClick={this.closeDialog} />

    var errorMessage = null
    if (this.state.errorMessage !== '') {
      errorMessage = <ErrorMessage message={this.state.errorMessage} />
    }

    return (
      <div className="med-dialog">
        <i className="bx bxs-save" />
        <h1>Save Selected Data</h1>
        <span className="med-description">
          Give a name to this selection of data points to save the selected
          data. Selection names can only contain Latin characters, digits,
          dashes (-), underscores (_), and spaces.
        </span>

        <div className="med-save-form">
          <input
            onChange={this.handleChange}
            type="text"
            id="name"
            className="med-text-input"
            placeholder="Selection name"
          />
        </div>

        {errorMessage}

        <button className="med-primary-solid accept" onClick={this.handleSave}>
          Save selection
        </button>
        <button className="med-cancel-button" onClick={this.closeDialog}>
          Cancel
        </button>
      </div>
    )
  }
}

export default SaveDialog
