// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
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
