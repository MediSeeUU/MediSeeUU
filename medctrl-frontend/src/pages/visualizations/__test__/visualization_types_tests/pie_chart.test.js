// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'
import ReactDOM from 'react-dom'
import getUniqueCategories from '../../single_visualization/utils/getUniqueCategories'
import sortCategoryData from '../../single_visualization/utils/sortCategoryData'
import generatePieSeries from '../../single_visualization/data_interfaces/generatePieSeries'
import PieChart from '../../single_visualization/visualization_types/PieChart'
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
  settings = { chartSpecificOptions, data }

  series = generatePieSeries(settings)
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
