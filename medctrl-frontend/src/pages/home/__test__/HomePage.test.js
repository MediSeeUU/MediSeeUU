import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter } from 'react-router-dom'
import HomePage from '../HomePage'
import { fireEvent, screen, render } from '@testing-library/react'
import MockProvider from '../../../mocks/MockProvider'

test('homepage renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <MockProvider>
        <HomePage />
      </MockProvider>
    </BrowserRouter>,
    root
  )
})

test('homepage search bar responds correctly', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <HomePage />
      </MockProvider>
    </BrowserRouter>
  )
  const input = screen.getByRole('textbox')
  fireEvent.change(input, { target: { value: 'pfizer' } })
  const search = screen.getByText('Search')
  expect(fireEvent.click(search)).toBeTruthy()
})
