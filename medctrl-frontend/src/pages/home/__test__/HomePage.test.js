import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter } from 'react-router-dom'
import HomePage from '../HomePage'
import { fireEvent, screen, render } from '@testing-library/react'
import { TableUtilsContext, TableUtilsUpdateContext } from '../../../shared/contexts/DataContext'

test('homepage renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <HomePage />
    </BrowserRouter>,
    root
  )
})

test('homepage search bar responds correctly', () => {
  const update = (utils) => {
    expect(utils.search).toStrictEqual(new String('pfizer'))
  }
  render(
    <BrowserRouter>
      <TableUtilsContext.Provider value={{search: ''}}>
        <TableUtilsUpdateContext.Provider value={update}>
          <HomePage />
        </TableUtilsUpdateContext.Provider>
      </TableUtilsContext.Provider>
    </BrowserRouter>
  )
  const input = screen.getByRole('textbox')
  fireEvent.change(input, { target: { value: 'pfizer' } })
  fireEvent.click(screen.getByText('Search'))
})
