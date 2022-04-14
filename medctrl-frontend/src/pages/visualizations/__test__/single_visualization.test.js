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

import data from '../data.json'

jest.mock('../mocks/observer')

test('render initial single visualization', () => {
  const handleChange = jest.fn()
  render(<SingleVisualization id={1} data={data} onChange={handleChange}/>)
  const dropdown = screen.getByRole('combobox', { name: 'Visualization type' })
  fireEvent.change(dropdown, { target: { value: 'line' }})
  //expect(screen.getByRole('combobox', { name: 'Visualization type' }).value).toMatch('line')
})

/* test('export to svg', () => {
  render(<SingleVisualization id={1} data={data} />)
  fireEvent.click(screen.getByRole('button', { name: 'Export as SVG'}))
}) */
