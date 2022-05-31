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
import GenerateLineSeries from '../../single_visualization/data_interfaces/LineInterface'
import LineChart from '../../single_visualization/visualization_types/LineChart'
import ResizeObserver from '../../mocks/observer'

import data from '../../../../testJson/data.json'

jest.mock('../../mocks/observer')

let container
let series
let settings
let chartSpecificOptions
const uniqueCategories = GetUniqueCategories(data)

beforeEach(() => {
  container = document.createElement('div')
  document.body.append(container)

  chartSpecificOptions = {
    xAxis: 'DecisionYear',
    yAxis: 'Rapporteur',
    categoriesSelectedX: uniqueCategories['DecisionYear'],
    categoriesSelectedY: ['United Kingdom'],
  },
  settings = { chartSpecificOptions, data }

  series = GenerateLineSeries(settings)
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

test('initial render with usual initialization', () => {
  ReactDOM.render(
    <LineChart
      legend={false}
      labels={false}
      id={1}
      series={series}
      categories={sortCategoryData(
        chartSpecificOptions.categoriesSelectedX
      )}
      options={chartSpecificOptions}
    />,
    container
  )
})
