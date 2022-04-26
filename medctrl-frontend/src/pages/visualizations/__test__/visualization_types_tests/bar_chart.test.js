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
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'
import GenerateBarSeries from '../../single_visualization/data_interfaces/BarInterface'
import BarChart from '../../single_visualization/visualization_types/BarChart'
import ResizeObserver from '../../mocks/observer'

import data from '../../../../testJson/data.json'

jest.mock('../../mocks/observer')

let container
let series
let uniqueCategories
let options

beforeEach(() => {
  container = document.createElement('div')
  document.body.append(container)

  let chartSpecificOptions = {
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelected: ['United Kingdom'],
    },
  }
  uniqueCategories = GetUniqueCategories(data)
  series = GenerateBarSeries(chartSpecificOptions, uniqueCategories, data)
  options = {
    stacked: false,
    stackType: '',
    horizontal: false,
  }
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

test('initial render with usual initialization', () => {
  ReactDOM.render(
    <BarChart
      key={1}
      legend={false}
      labels={false}
      id={1}
      series={series}
      categories={uniqueCategories['DecisionYear']}
      options={options}
    />,
    container
  )
})

test('initial render with stackType: 100%', () => {
  options = {
    stacked: false,
    stackType: '100%',
    horizontal: false,
  }
  ReactDOM.render(
    <BarChart
      key={1}
      legend={false}
      labels={false}
      id={1}
      series={series}
      categories={uniqueCategories['DecisionYear']}
      options={options}
    />,
    container
  )
})

test('error handler test', () => {
  ReactDOM.render(
    <BarChart
      key={1}
      legend={false}
      labels={false}
      id={1}
      series={null}
      categories={uniqueCategories['DecisionYear']}
      options={options}
    />,
    container
  )
  expect(
    screen.queryByText('An error occurred when drawing the chart')
  ).not.toBe(null)
})
