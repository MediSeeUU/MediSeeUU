import React from 'react'
import { render, screen, within } from '@testing-library/react'
import SavedSelections from '../SavedSelections'
import MockProvider from '../../../../mocks/mockProvider'

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
