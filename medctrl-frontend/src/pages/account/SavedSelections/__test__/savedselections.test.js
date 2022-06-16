// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen, within } from '@testing-library/react'
import SavedSelections from '../SavedSelections'
import MockProvider from '../../../../mocks/MockProvider'

test('SavedSelections renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <MockProvider>
      <SavedSelections />
    </MockProvider>,
    root
  )
})

test('component has correct number of rows', async () => {
  const value = await fetch('/api/saveselection').then((x) => x.json())
  render(
    <MockProvider>
      <SavedSelections />
    </MockProvider>
  )
  const table = await screen.findByRole('table')
  const rows = within(table).getAllByRole('row')
  expect(rows).toHaveLength(value.length + 1)
})
