import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent } from '@testing-library/react'
import ExportMenu from '../ExportMenu'
import DummyData from '../../../../testJson/small_data.json'
import { SelectedContext } from '../../../../shared/contexts/DataContext'

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
})

// when the user selects any of the first four possible export
// file types and presses the download button, the user should
// be redirected to a succes message screen
test('valid selection download should result in UI success message', () => {
  const view = render(
    <SelectedContext.Provider value={DummyData}>
      <ExportMenu />
    </SelectedContext.Provider>
  )
  fireEvent.click(screen.getByText('Export'))
  const option = screen.getAllByRole('radio')[0]
  const downloadButton = screen.getByText('Download')
  fireEvent.click(option)
  fireEvent.click(downloadButton)
  const dialogHeader = screen.getByRole('heading')
  expect(dialogHeader.innerHTML).toBe('Export Successfull')
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
  const option = screen.getAllByRole('radio')[4]
  const downloadButton = screen.getByText('Download')
  fireEvent.click(option)
  fireEvent.click(downloadButton)
  const dialogHeader = screen.getByRole('heading')
  expect(dialogHeader.innerHTML).toBe('Export Selected Data')
  const errorContainer = screen.getByText('An Error Occurred')
  expect(errorContainer).toBeTruthy()
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
  const option = screen.getAllByRole('radio')[4]
  const textField = screen.getByRole('textbox')
  const downloadButton = screen.getByText('Download')
  fireEvent.click(option)
  fireEvent.change(textField, { target: { value: '|' } })
  fireEvent.click(downloadButton)
  const dialogHeader = screen.getByRole('heading')
  expect(dialogHeader.innerHTML).toBe('Export Successfull')
})
