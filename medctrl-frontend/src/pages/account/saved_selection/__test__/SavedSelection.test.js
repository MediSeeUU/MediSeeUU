// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent } from '@testing-library/react'
import SavedSelection from '../SavedSelection'
import MockProvider from '../../../../mocks/MockProvider'

const selection = {
  id: '377932a8-63e6-4e77-bb0f-efc220eb6d25',
  name: 'test1',
  created_at: '2022-05-17T11:16:47.141360Z',
  created_by: 'admin',
  eu_pnumbers: [1, 2, 3],
}

test('SavedSelections renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <MockProvider>
      <table>
        <tbody>
          <SavedSelection savedSelection={selection} />
        </tbody>
      </table>
    </MockProvider>,
    root
  )
})

test('apply selection is pressed', () => {
  render(
    <MockProvider>
      <table>
        <tbody>
          <SavedSelection savedSelection={selection} />
        </tbody>
      </table>
    </MockProvider>
  )
  const update = screen.getByTestId('update-select')
  expect(fireEvent.click(update)).toBeTruthy()
})

test('delete selection is pressed', () => {
  render(
    <MockProvider>
      <table>
        <tbody>
          <SavedSelection savedSelection={selection} />
        </tbody>
      </table>
    </MockProvider>
  )
  const remove = screen.getByTestId('delete-select')
  expect(fireEvent.click(remove)).toBeTruthy()
})
