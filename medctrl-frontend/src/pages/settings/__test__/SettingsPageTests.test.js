import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import SettingsPage from '../SettingsPage'

test('render settings page without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <SettingsPage />
    </BrowserRouter>,
    root
  )
})

test('submit color settings form', () => {
  render(
    <BrowserRouter>
      <SettingsPage />
    </BrowserRouter>
  )
  const applyButton = screen.getByText('Apply')
  fireEvent.click(applyButton)
})
