import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent } from '@testing-library/react'
import SaveMenu from '../SaveMenu'
import DummyData from '../../../../testJson/small_data.json'
import { SelectedContext } from '../../../../shared/contexts/DataContext'

// the save dialog should render without crashing
test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <SelectedContext.Provider value={DummyData}>
      <SaveMenu />
    </SelectedContext.Provider>,
    root
  )
})

// when the user provides a valid name, the user should be redirected to a
// success message screen
test('valid selection name should result in UI success message', () => {
  const validNames = ['Test', 'COVID-19', 'Special_set', 'Demo selection']
  const view = render(
    <SelectedContext.Provider value={DummyData}>
      <SaveMenu selectedData={DummyData} />
    </SelectedContext.Provider>
  )
  for (let i = 0; i < validNames.length; i++) {
    fireEvent.click(screen.getByText('Save'))
    const saveName = screen.getByPlaceholderText('Selection name')
    fireEvent.change(saveName, {
      target: { value: validNames[i] },
    })
    const saveButton = screen.getByText('Save selection')
    fireEvent.click(saveButton)
    const dialogHeader = screen.getByRole('heading')
    expect(dialogHeader.innerHTML).toBe('Selection Successfully Saved')
    const doneButton = screen.getByText('Done')
    fireEvent.click(doneButton)
  }
})

// when the user provides an invalid name, the user should be redirected to an
// error message screen
test('invalid selection name should result in UI error message', () => {
  const invalidNames = [
    'Test!',
    'COVID-19,',
    '(Special)_set',
    'Demo selection.',
  ]
  const view = render(
    <SelectedContext.Provider value={DummyData}>
      <SaveMenu selectedData={DummyData} />
    </SelectedContext.Provider>
  )
  for (let i = 0; i < invalidNames.length; i++) {
    fireEvent.click(screen.getByText('Save'))
    const saveName = screen.getByPlaceholderText('Selection name')
    fireEvent.change(saveName, {
      target: { value: invalidNames[i] },
    })
    const saveButton = screen.getByText('Save selection')
    fireEvent.click(saveButton)
    const dialogHeader = screen.getByRole('heading')
    expect(dialogHeader.innerHTML).toBe('Save Selected Data')
    const errorContainer = screen.getByText('An Error Occurred')
    expect(errorContainer).toBeTruthy()
    const cancelButton = screen.getByText('Cancel')
    fireEvent.click(cancelButton)
  }
})
