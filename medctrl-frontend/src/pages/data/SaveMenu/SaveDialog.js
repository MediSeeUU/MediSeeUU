import React from 'react'

import ErrorDialog from './SaveMenuComponents/ErrorDialog'
import SuccessDialog from './SaveMenuComponents/SuccessDialog'
import ErrorMessage from './SaveMenuComponents/ErrorMessage'

import postSavedSelection from './SaveHandler'

class SaveDialog extends React.Component {
  // Save Dialog is a class based component. it is passed some series of
  // data points, and it allows the user to save these points as a selection
  // with a name
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

  // method used for the handling the closing of the save dialog
  closeDialog() {
    this.state.onClose()
  }

  // method used for handling when the user presses the save button
  // first it is checked if the current dialog state is valid, if so the
  // data is saved, otherwise an error is displayed
  handleSave(event) {
    event.preventDefault()

    // EUNoShorts of selected data points
    var eunumbers = []
    this.selectedData.forEach((dataPoint) =>
      eunumbers.push(dataPoint.EUNoShort)
    )

    // check whether the name field has input
    if (this.state.saveName === '') {
      this.setState({ errorMessage: this.noSaveName })
      return
    }

    // check whether only allowed characters are used
    if (!/^[A-Za-z0-9\-_ ]*$/.test(this.state.saveName)) {
      this.setState({ errorMessage: this.invalidName })
      return
    }

    try {
      postSavedSelection(eunumbers, this.state.saveName)
    } catch {
      this.setState({ dialogState: 'error' })
      return
    }

    this.setState({ dialogState: 'success' })
  }

  // when the user updates the input field in the dialog,
  // this method is used to update the current state of the dialog
  // to reflect this user interaction
  handleChange(event) {
    this.setState({ saveName: event.target.value })
  }

  // depending on the state of the dialog, a specific dialog is rendered
  // if the user has given a valid name, the selection is saved
  // (success) or an error has occurred (error). if any error messages need
  // to be displayed in the default view these are added dynamically
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
      <div className="med-save-dialog">
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
