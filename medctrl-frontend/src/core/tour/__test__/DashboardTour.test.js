// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import { fireEvent, render, screen } from '@testing-library/react'
import App from '../../app/App'

test('First tour rooltip is correct', () => {
  render(<App />)
  const tourButton = screen.getByText('Start Tour')
  fireEvent.click(tourButton)
  expect(screen.getByText('Quick Search')).toBeTruthy()
  fireEvent.click(screen.getByText('End'))
})

test('Can move to next tour tooltip', () => {
  render(<App />)
  const tourButton = screen.getByText('Start Tour')
  fireEvent.click(tourButton)
  fireEvent.click(screen.getByText('Next'))
  fireEvent.click(screen.getByText('End'))
  expect(screen.getByText('Dashboard Tour')).toBeTruthy()
})

test('Ending the tour redirect to the home page', () => {
  render(<App />)
  const tourButton = screen.getByText('Start Tour')
  fireEvent.click(tourButton)
  fireEvent.click(screen.getByText('End'))
  expect(screen.getByText('Dashboard Tour')).toBeTruthy()
})
