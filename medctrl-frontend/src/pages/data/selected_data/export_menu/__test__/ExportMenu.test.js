// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent } from '@testing-library/react'
import ExportMenu from '../ExportMenu'
import DummyData from '../../../../../json/small_data.json'
import MockProvider from '../../../../../mocks/MockProvider'

// This is required to make sure the tests don't crash
// when the tested components try and download a file
jest.mock('file-saver', () => ({ saveAs: jest.fn() }))

// The export dialog should render without crashing
test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <MockProvider>
      <ExportMenu selectedData={DummyData} />
    </MockProvider>,
    root
  )
})

// When the user does not select any option and presses the download button,
// the user should see an error message on screen
test('no selection should result in UI error message', () => {
  render(
    <MockProvider>
      <ExportMenu selectedData={DummyData} />
    </MockProvider>
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

// When the user selects any of the first four possible export
// file types and presses the download button, the user should
// be redirected to a succes message screen
test('valid selection download should result in UI success message', () => {
  const validOptions = [
    'Excel File (.xlsx)',
    'Comma Separated (.csv)',
    'Tab Separeted (.tsv)',
    'Semicolon Separeted (.ssv)',
  ]
  render(
    <MockProvider>
      <ExportMenu selectedData={DummyData} />
    </MockProvider>
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

// When the user selects the custom delimited option, but does not
// specify a custom separator, the user should see an error message on screen
test('custom selection without separator should result in UI error message', () => {
  render(
    <MockProvider>
      <ExportMenu selectedData={DummyData} />
    </MockProvider>
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

// When the user selects the custom delimited option, and specifies a
// custom separator,the user should be redirected to a succes message screen
test('custom selection with separator should result in UI success message', () => {
  render(
    <MockProvider>
      <ExportMenu selectedData={DummyData} />
    </MockProvider>
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

// When one of the radio buttons is manipulated to contain an incorrect
// id, the no file type can corretly be selected and the file export
// fails, this will be reflected by an error dialog
test('download attempt with invalid selection should result in error dialog', () => {
  render(
    <MockProvider>
      <ExportMenu selectedData={DummyData} />
    </MockProvider>
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
