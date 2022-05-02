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
import GenerateLineSeries from '../../single_visualization/data_interfaces/LineInterface'
import LineChart from '../../single_visualization/visualization_types/LineChart'
import ResizeObserver from '../../mocks/observer'

import data from '../../../../testJson/data.json'

jest.mock('../../mocks/observer')

let container
let series
let uniqueCategories

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
  series = GenerateLineSeries(chartSpecificOptions, uniqueCategories, data)
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

test('initial render with usual initialization', () => {
  ReactDOM.render(
    <LineChart
      key={1}
      legend={false}
      labels={false}
      id={1}
      series={series}
      categories={uniqueCategories['DecisionYear']}
      options={{}}
    />,
    container
  )
})

test('error handler test', () => {
  ReactDOM.render(
    <LineChart
      key={1}
      legend={false}
      labels={false}
      id={1}
      series={null}
      categories={uniqueCategories['DecisionYear']}
      options={{}}
    />,
    container
  )
  expect(
    screen.queryByText('An error occurred when drawing the chart')
  ).not.toBe(null)
})
