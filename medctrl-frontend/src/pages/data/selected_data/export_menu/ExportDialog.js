// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import * as XLSX from 'xlsx'
import FileSaver from 'file-saver'
import ErrorDialog from './components/ErrorDialog'
import SuccessDialog from './components/SuccessDialog'
import ErrorMessage from './components/ErrorMessage'
import RadioElement from './components/RadioElement'

// Class based component which renders the export dialog
// It is passed some series of datapoints, and it allows the user
// to export these points in any of the available file types.
// A class is used instead of a function because of the extensive state.
class ExportDialog extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      dialogState: 'default',
      exportType: '',
      customSeparator: '',
      onClose: props.onClose,
      errorMessage: '',
    }

    this.selectedData = props.data

    this.noExportType =
      'No file type selected. Please select one of the above specified file types to be able to export the selected data.'
    this.noSeparator =
      'No separator given. Please specify a separator to be used in the custom delimited file format to be able to export the selected data.'

    this.closeDialog = this.closeDialog.bind(this)
    this.handleDownload = this.handleDownload.bind(this)
    this.exportData = this.exportData.bind(this)
    this.handleChange = this.handleChange.bind(this)
  }

  // Handler to close the dialog
  closeDialog() {
    this.state.onClose()
  }

  // Method used for handling when the user pressess the download button.
  // First it is checked if the current dialog state is valid, if so the
  // data is exported and downloaded, otherwise an error is displayed.
  handleDownload(event) {
    event.preventDefault()

    if (this.state.exportType === '') {
      this.setState({ errorMessage: this.noExportType })
      return
    }

    if (this.state.exportType === 'custom') {
      if (this.state.customSeparator === '') {
        this.setState({ errorMessage: this.noSeparator })
        return
      }
    }

    try {
      this.exportData()
    } catch {
      this.setState({ dialogState: 'error' })
      return
    }

    this.setState({ dialogState: 'success' })
  }

  // Exports all the datapoints contained in the selected data, according to
  // the given user preference. It assumes that the current state of
  // user preference is valid
  exportData() {
    const selectedData = this.selectedData
    const exportType = this.state.exportType

    // First convert the selected data points to a worksheet object
    const ws = XLSX.utils.json_to_sheet(selectedData)

    // - The actual data object which contains the formatted data points
    // - The final file extension in string format
    var data
    var extension

    // The worksheet object should be exported to an excel format
    if (exportType === 'xlsx') {
      const wb = { Sheets: { data: ws }, SheetNames: ['data'] }
      const excelBuffer = XLSX.write(wb, { bookType: 'xlsx', type: 'array' })
      data = new Blob([excelBuffer], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8',
      })
      extension = '.xlsx'
    }

    // The worksheet object should be exported to a custom delimited format
    else if (exportType === 'custom') {
      const separator = this.state.customSeparator
      data = new Blob([XLSX.utils.sheet_to_csv(ws, { FS: separator })])
      extension = '.txt'
    }

    // The worksheet object should be exported to a comma delimited format
    else if (exportType === 'csv') {
      data = new Blob([XLSX.utils.sheet_to_csv(ws, { FS: ',' })])
      extension = '.csv'
    }

    // The worksheet object should be exported to a tab delimited format
    else if (exportType === 'tsv') {
      data = new Blob([XLSX.utils.sheet_to_csv(ws, { FS: '\t' })])
      extension = '.tsv'
    }

    // The worksheet object should be exported to a semicolon delimited format
    else if (exportType === 'ssv') {
      data = new Blob([XLSX.utils.sheet_to_csv(ws, { FS: ';' })])
      extension = '.ssv'
    }

    // If something has gone wrong somewhere, an error will be displayed
    else {
      throw new Error('export type is not valid!')
    }

    FileSaver.saveAs(data, 'exported-medicine-data' + extension)
  }

  // When the user updates one of the input fields in the dialog,
  // this method is used to update the current state of the dialog
  // to reflect this user interaction
  handleChange(event) {
    const target = event.target.type
    const value = event.target.value
    const id = event.target.id

    if (target === 'radio') {
      this.setState({ exportType: id })
    }

    if (target === 'text' && id === 'separator') {
      this.setState({ customSeparator: value })
    }
  }

  // Depending on the state of the dialog, a specific dialog is rendered
  // if the user is giving a preference (default), the download is commencing
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
      <div className="med-export-dialog med-dialog">
        <i className="bx bxs-download" />
        <h1>Export Selected Data</h1>
        <span className="med-description">
          Choose one of the file types below to export the selected data, or
          specify a custom delimited file type.
        </span>

        <div className="med-download-option-list">
          <RadioElement
            onChange={this.handleChange}
            name="radio"
            id="xlsx"
            value="Excel File (.xlsx)"
          />
          <RadioElement
            onChange={this.handleChange}
            name="radio"
            id="csv"
            value="Comma Separated (.csv)"
          />
          <RadioElement
            onChange={this.handleChange}
            name="radio"
            id="tsv"
            value="Tab Separeted (.tsv)"
          />
          <RadioElement
            onChange={this.handleChange}
            name="radio"
            id="ssv"
            value="Semicolon Separeted (.ssv)"
          />
          <RadioElement
            onChange={this.handleChange}
            name="radio"
            id="custom"
            value="Custom Separator:"
          >
            <input
              onChange={this.handleChange}
              type="text"
              id="separator"
              className="med-seperator-input-field med-text-input"
            />
          </RadioElement>
        </div>

        {errorMessage}

        <button
          className="med-primary-solid accept"
          onClick={this.handleDownload}
        >
          Download
        </button>
        <button className="med-cancel-button" onClick={this.closeDialog}>
          Cancel
        </button>
      </div>
    )
  }
}

export default ExportDialog
