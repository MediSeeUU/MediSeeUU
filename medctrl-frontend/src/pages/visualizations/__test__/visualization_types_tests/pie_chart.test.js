// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
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
import GeneratePieSeries from '../../single_visualization/data_interfaces/PieInterface'
import PieChart from '../../single_visualization/visualization_types/PieChart'
import ResizeObserver from '../../mocks/observer'

import data from '../../../../testJson/data.json'

jest.mock('../../mocks/observer')

let container
let series
let chartSpecificOptions

beforeEach(() => {
  container = document.createElement('div')
  document.body.append(container)

  chartSpecificOptions = {
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: ['United Kingdom'],
    },
  }
  series = GeneratePieSeries(chartSpecificOptions, data)
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

test('initial render with usual initialization', () => {
  ReactDOM.render(
    <PieChart
      key={1}
      legend={false}
      labels={false}
      id={1}
      series={series}
      categories={sortCategoryData(
        chartSpecificOptions.chartSpecificOptions.categoriesSelectedX
      )}
      options={{}}
    />,
    container
  )
})
