import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter } from 'react-router-dom'
import HomePage from '../HomePage'
import { fireEvent, screen, render } from '@testing-library/react'

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
  render(
    <BrowserRouter>
      <HomePage />
    </BrowserRouter>
  )
  fireEvent.click(screen.getByText('Search'))
})
