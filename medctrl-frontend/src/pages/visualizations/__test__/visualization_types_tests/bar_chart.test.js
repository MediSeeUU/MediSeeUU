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
import sortCategoryData from '../../single_visualization/utils/SortCategoryData'
import GenerateBarSeries from '../../single_visualization/data_interfaces/BarInterface'
import BarChart from '../../single_visualization/visualization_types/BarChart'
import ResizeObserver from '../../mocks/observer'

import data from '../../../../testJson/data.json'

jest.mock('../../mocks/observer')

let container
let series
let uniqueCategories = GetUniqueCategories(data)
let options
let chartSpecificOptions

beforeEach(() => {
  container = document.createElement('div')
  document.body.append(container)

  chartSpecificOptions = {
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelectedX: uniqueCategories['DecisionYear'],
      categoriesSelectedY: ['United Kingdom'],
    },
  }
  series = GenerateBarSeries(chartSpecificOptions, data)
  options = {
    stacked: false,
    stackType: false,
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
      categories={sortCategoryData(
        chartSpecificOptions.chartSpecificOptions.categoriesSelectedX
      )}
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
      categories={sortCategoryData(
        chartSpecificOptions.chartSpecificOptions.categoriesSelectedX
      )}
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
      categories={sortCategoryData(
        chartSpecificOptions.chartSpecificOptions.categoriesSelectedX
      )}
      options={options}
    />,
    container
  )
  expect(
    screen.queryByText('An error occurred when drawing the chart')
  ).not.toBe(null)
})
