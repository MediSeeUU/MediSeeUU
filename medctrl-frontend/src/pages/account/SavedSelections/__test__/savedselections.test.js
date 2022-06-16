// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'
import { render, screen, within } from '@testing-library/react'
import SavedSelections from '../SavedSelections'
import MockProvider from '../../../../mocks/MockProvider'

test('Component has correct number of rows', async () => {
  let value = await fetch('/api/saveselection').then((x) => x.json())
  render(
    <MockProvider>
      <SavedSelections />
    </MockProvider>
  )

  let r = await screen.findByRole('table')
  const rows = within(r).getAllByRole('row')
  expect(rows).toHaveLength(value.length + 1)
})
