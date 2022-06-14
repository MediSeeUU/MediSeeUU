import React from 'react'
import ReactDOM from 'react-dom'
import getUniqueCategories from '../../single_visualization/utils/getUniqueCategories'
import sortCategoryData from '../../single_visualization/utils/sortCategoryData'
import generateHistogramSeries from '../../single_visualization/data_interfaces/generateHistogramSeries'
import HistogramChart from '../../single_visualization/visualization_types/HistogramChart'
import ResizeObserver from '../../mocks/observer'

import data from '../../../../json/data.json'

jest.mock('../../mocks/observer')

let container
const unique = getUniqueCategories(data)
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

  series = generateHistogramSeries(settings)
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
