import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent } from '@testing-library/react'
import ExportMenu from '../ExportMenu'
import DummyData from '../../../../testJson/small_data.json'
import { SelectedContext } from '../../../../shared/contexts/DataContext'

// this is required to make sure the tests don't crash
// when the tested components try and download a file
jest.mock('file-saver', () => ({ saveAs: jest.fn() }))

// the export dialog should render without crashing
test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <SelectedContext.Provider value={DummyData}>
      <ExportMenu />
    </SelectedContext.Provider>,
    root
  )
})

// when the user does not select any option and presses the download button,
// the user should see an error message on screen
test('no selection should result in UI error message', () => {
  const view = render(
    <SelectedContext.Provider value={DummyData}>
      <ExportMenu />
    </SelectedContext.Provider>
  )
  fireEvent.click(screen.getByText('Export'))
  const downloadButton = screen.getByText('Download')
  fireEvent.click(downloadButton)
  const dialogHeader = screen.getByRole('heading')
  expect(dialogHeader.innerHTML).toBe('Export Selected Data')
  const errorContainer = screen.getByText('An Error Occurred')
  expect(errorContainer).toBeTruthy()
  const cancelButton = screen.getByText('Cancel')
  fireEvent.click(cancelButton)
})

// when the user selects any of the first four possible export
// file types and presses the download button, the user should
// be redirected to a succes message screen
test('valid selection download should result in UI success message', () => {
  const validOptions = [
    'Excel File (.xlsx)',
    'Comma Separated (.csv)',
    'Tab Separeted (.tsv)',
    'Semicolon Separeted (.ssv)',
  ]
  const view = render(
    <SelectedContext.Provider value={DummyData}>
      <ExportMenu />
    </SelectedContext.Provider>
  )
  for (let i = 0; i < validOptions.length; i++) {
    fireEvent.click(screen.getByText('Export'))
    const option = screen.getByText(validOptions[i])
    const downloadButton = screen.getByText('Download')
    fireEvent.click(option)
    fireEvent.click(downloadButton)
    const dialogHeader = screen.getByRole('heading')
    expect(dialogHeader.innerHTML).toBe('Export Successfull')
    const doneButton = screen.getByText('Done')
    fireEvent.click(doneButton)
  }
})

// when the user selects the custom delimited option, but does not
// specify a custom separator, the user should see an error message on screen
test('custom selection without separator should result in UI error message', () => {
  const view = render(
    <SelectedContext.Provider value={DummyData}>
      <ExportMenu />
    </SelectedContext.Provider>
  )
  fireEvent.click(screen.getByText('Export'))
  const option = screen.getByText('Custom Separator:')
  const downloadButton = screen.getByText('Download')
  fireEvent.click(option)
  fireEvent.click(downloadButton)
  const dialogHeader = screen.getByRole('heading')
  expect(dialogHeader.innerHTML).toBe('Export Selected Data')
  const errorContainer = screen.getByText('An Error Occurred')
  expect(errorContainer).toBeTruthy()
  const cancelButton = screen.getByText('Cancel')
  fireEvent.click(cancelButton)
})

// when the user selects the custom delimited option, and specifies a
// custom separator,the user should be redirected to a succes message screen
test('custom selection with separator should result in UI success message', () => {
  const view = render(
    <SelectedContext.Provider value={DummyData}>
      <ExportMenu />
    </SelectedContext.Provider>
  )
  fireEvent.click(screen.getByText('Export'))
  const option = screen.getByText('Custom Separator:')
  const textField = screen.getByRole('textbox')
  const downloadButton = screen.getByText('Download')
  fireEvent.click(option)
  fireEvent.change(textField, { target: { value: '|' } })
  fireEvent.click(downloadButton)
  const dialogHeader = screen.getByRole('heading')
  expect(dialogHeader.innerHTML).toBe('Export Successfull')
})

// when one of the radio buttons is manipulated to contain an incorrect
// id, the no file type can corretly be selected and the file export
// fails, this will be reflected by an error dialog
test('download attempt with invalid selection should result in error dialog', () => {
  const view = render(
    <SelectedContext.Provider value={DummyData}>
      <ExportMenu />
    </SelectedContext.Provider>
  )
  fireEvent.click(screen.getByText('Export'))
  const radio = screen.getAllByRole('radio')[0]
  radio.id = 'invalid'
  fireEvent.click(radio)
  const downloadButton = screen.getByText('Download')
  fireEvent.click(downloadButton)
  const dialogHeader = screen.getByRole('heading')
  expect(dialogHeader.innerHTML).toBe('An Error Occurred')
})
