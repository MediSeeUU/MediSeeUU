import React from 'react'
import ReactDOM from 'react-dom'
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'
import sortCategoryData from '../../single_visualization/utils/SortCategoryData'
import GeneratePieSeries from '../../single_visualization/data_interfaces/PieInterface'
import PieChart from '../../single_visualization/visualization_types/PieChart'
import ResizeObserver from '../../mocks/observer'

import data from '../../../../testJson/data.json'

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
  settings = { chartSpecificOptions, data }

  series = GeneratePieSeries(settings)
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

test('initial render with usual initialization', () => {
  ReactDOM.render(
    <PieChart
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
