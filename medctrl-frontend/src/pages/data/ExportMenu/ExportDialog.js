import React from 'react'
import * as XLSX from 'xlsx'
import FileSaver from 'file-saver'

import ErrorDialog from './ExportMenuComponents/ErrorDialog'
import SuccessDialog from './ExportMenuComponents/SuccessDialog'
import ErrorMessage from './ExportMenuComponents/ErrorMessage'
import RadioElement from './ExportMenuComponents/RadioElement'

class ExportDialog extends React.Component {
  // Export Dialog is a class based component. it is passed some series of
  // datapoints, and it allowes the user to export these point in any of the
  // available file types
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
      'No file type selected. Please select on of the above spefied file types, to be able to export the selected data.'
    this.noSeparator =
      'No separator given. Please specify a separator to be used in the custom delimited file format, to be able to export the selected data.'

    this.closeDialog = this.closeDialog.bind(this)
    this.handleDownload = this.handleDownload.bind(this)
    this.exportData = this.exportData.bind(this)
    this.handleChange = this.handleChange.bind(this)
  }

  // method used for the handling the closing of the export dialog
  closeDialog() {
    this.state.onClose()
  }

  // method used for handling when the user pressess the download button
  // first it is checked if the current dialog state is valid, if so the
  // data is exported and downloaded, otherwise an error is displayed
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
      return;
    }

    this.setState({ dialogState: 'success' })
  }

  // exports all the datapoints contained in this.selectedData, according to
  // the given user preference. this methd assumes that the current state of
  // user preference is valid
  exportData() {
    const selectedData = this.selectedData
    const exportType = this.state.exportType

    // first convert the selected data points to a worksheet object
    const ws = XLSX.utils.json_to_sheet(selectedData)

    // - the actual data object which contains the formatted data points
    // - the final file extension in string format
    var data
    var extension

    // the worksheet object should be exported to an excel format
    if (exportType === 'xlsx') {
      const wb = { Sheets: { data: ws }, SheetNames: ['data'] }
      const excelBuffer = XLSX.write(wb, { bookType: 'xlsx', type: 'array' })
      data = new Blob([excelBuffer], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=UTF-8',
      })
      extension = '.xlsx'
    }

    // the worksheet object should be exported to a custom delimited format
    else if (exportType === 'custom') {
      const separator = this.state.customSeparator
      data = new Blob([XLSX.utils.sheet_to_csv(ws, { FS: separator })])
      extension = '.txt'
    }

    // the worksheet object should be exported to a comma delimited format
    else if (exportType === 'csv') {
      data = new Blob([XLSX.utils.sheet_to_csv(ws, { FS: ',' })])
      extension = '.csv'
    }

    // the worksheet object should be exported to a tab delimited format
    else if (exportType === 'tsv') {
      data = new Blob([XLSX.utils.sheet_to_csv(ws, { FS: '\t' })])
      extension = '.tsv'
    }

    // the worksheet object should be exported to a semicolon delimited format
    else if (exportType === 'ssv') {
      data = new Blob([XLSX.utils.sheet_to_csv(ws, { FS: ';' })])
      extension = '.ssv'
    }

    // if something has gone wrong somewhere, an error will be displayed
    else {
      throw new Error('export type is not valid!')
    }

    FileSaver.saveAs(data, 'exported-medicine-data' + extension)
  }

  // when the user updates one of the input fields in the dialog,
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

  // depending on the state of the dialog, a specific dialog is rendered
  // if the user is giving a preference (default), the download is commencing
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
      <div className="export-dialog">
        <i className="bx bxs-download" />
        <h1>Export Selected Data</h1>
        <span className="desc">
          Choose one of the file types below to export the selected data, or
          specify a custom delimited file type.
        </span>

        <div className="option-list">
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
              className="text-input"
            />
          </RadioElement>
        </div>

        {errorMessage}

        <button className="accept" onClick={this.handleDownload}>
          Download
        </button>
        <button className="cancel" onClick={this.closeDialog}>
          Cancel
        </button>
      </div>
    )
  }
}

export default ExportDialog
