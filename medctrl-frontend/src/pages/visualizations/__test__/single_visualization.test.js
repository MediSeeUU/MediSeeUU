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
import UserEvent from '@testing-library/user-event'
import GetUniqueCategories from '../single_visualization/utils/GetUniqueCategories'

import data from '../../../testJson/data.json'
import { act, createRenderer, renderIntoDocument } from 'react-dom/test-utils'

jest.mock('../mocks/observer')

test('render initial single visualization', () => {
  const root = document.createElement('div')
  document.body.append(root)
  ReactDOM.render(<SingleVisualization id={1} data={data} />, root)
})

test('export to svg', () => {
  const root = document.createElement('div')
  ReactDOM.render(<SingleVisualization id={1} data={data} />, root)
  fireEvent.click(screen.getByRole('button', { name: 'Export as SVG' }))
})

test('change chart type', () => {
  const root = document.createElement('div')
  let vis = ReactDOM.render(<SingleVisualization id={1} data={data} />, root)
  const chartSpecificOptions = {
    xAxis: 'DecisionYear',
    yAxis: 'Rapporteur',
    categoriesSelected: ['United Kingdom'],
    stackType: 'normal',
    stacked: false,
    horizontal: false,
  }
  const event = {
    chart_type: 'line',
    chartSpecificOptions: chartSpecificOptions,
    legend_on: false,
    label_on: false,
    chartSpecificOptionsName: '',
  }

  expect(() => vis.handleChange(event)).toThrow()
})
