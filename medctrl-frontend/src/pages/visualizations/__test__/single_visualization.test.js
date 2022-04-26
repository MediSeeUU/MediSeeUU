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
import SingleVisualization from '../single_visualization/SingleVisualization'
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

test('render initial single visualization', () => {
  ReactDOM.render(<SingleVisualization id={1} data={data} />, container)
})

test('export to svg', () => {
  ReactDOM.render(<SingleVisualization id={1} data={data} />, container)
  fireEvent.click(screen.getByRole('button', { name: 'Export as SVG' }))
})

test('export to png', () => {
  ReactDOM.render(<SingleVisualization id={1} data={data} />, container)
  fireEvent.click(screen.getByRole('button', { name: 'Export as PNG' }))
})

test('remove itself', () => {
  const onRemoval = jest.fn()
  ReactDOM.render(<SingleVisualization id={1} data={data} onRemoval={onRemoval}/>, container)
  fireEvent.click(screen.getByRole('button', { name: '' }))
})