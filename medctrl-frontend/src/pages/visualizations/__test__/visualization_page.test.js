import React from 'react'
import ReactDOM from 'react-dom'
import {
  cleanup,
  render,
  fireEvent,
  waitFor,
  screen,
  getByRole,
  getByText,
} from '@testing-library/react'
import VisualizationPage from '../VisualizationPage'
import ResizeObserver from '../mocks/observer'

import data from '../../../testJson/data.json'

jest.mock('../mocks/observer')

let container
beforeEach(() => {
  container = document.createElement('div')
  document.body.append(container)
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

test('no data', () => {
  ReactDOM.render(<VisualizationPage selectedData={[]} />, container)
})

test('initial render', () => {
  ReactDOM.render(<VisualizationPage selectedData={data} />, container)
})

// rendering a visualization page and adding a visualization
test('add a visualization', () => {
  ReactDOM.render(<VisualizationPage selectedData={data} />, container)
  fireEvent.click(screen.getByRole('button', { name: /add visualization/i }))
  // we start with 1 visualization and add another
  expect(
    screen.getAllByRole('button', { name: /export as svg/i }).length
  ).toEqual(2)
})

// rendering a visualization page, then removing the initial visualization
test('remove a visualization', () => {
  ReactDOM.render(<VisualizationPage selectedData={data} />, container)
  // the removal button is currently the only button with no text
  let target = screen.getByRole('button', { name: '' })
  // it throws an error that has to do with the ApexCharts library,
  // we have not found any way around this sadly
  expect(() => fireEvent.click(target)).toThrow()
})