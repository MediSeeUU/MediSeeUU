import React from 'react'
import ReactDOM from 'react-dom'
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'
import sortCategoryData from '../../single_visualization/utils/SortCategoryData'
import GenerateHistogramSeries from '../../single_visualization/data_interfaces/HistogramInterface'
import HistogramChart from '../../single_visualization/visualization_types/HistogramChart'
import ResizeObserver from '../../mocks/observer'

import data from '../../../../json/data.json'

jest.mock('../../mocks/observer')

let container
const unique = GetUniqueCategories(data)
let series
let settings
let chartSpecificOptions

beforeEach(() => {
  container = document.createElement('div')
  document.body.append(container)

  chartSpecificOptions = {
    xAxis: 'Rapporteur',
    categoriesSelectedX: unique['Rapporteur'],
  }

  settings = {
    chartSpecificOptions,
    data,
  }

  series = GenerateHistogramSeries(settings)
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

test('initial render', () => {
  ReactDOM.render(
    <HistogramChart
      legend={false}
      labels={false}
      id={1}
      series={series}
      categories={sortCategoryData(chartSpecificOptions.categoriesSelectedX)}
      options={chartSpecificOptions}
    />,
    container
  )
})
