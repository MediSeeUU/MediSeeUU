// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter } from 'react-router-dom'
import HomePage from '../HomePage'
import { fireEvent, screen, render } from '@testing-library/react'
import {
  TableUtilsContext,
  TableUtilsUpdateContext,
} from '../../../shared/contexts/DataContext'

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
      <TableUtilsContext.Provider value={{ search: '' }}>
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
