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

import data from '../data.json'
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

test('check whether the initial render works', () => {
  const root = document.createElement('div')
  const vis = ReactDOM.render(<SingleVisualization id={1} data={data} />, root)
  const dropdown = screen.getByRole('combobox', { name: /visualization type/i })
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
  const change = () => vis.handleChange(event)
  change
  setTimeout(() => {
    expect(vis.state.chart_type).toBe('line')
  }, 50)

  //expect(screen.getByRole('combobox', { name: 'Visualization type' }).value).toMatch('line')
})
