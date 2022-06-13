import React from 'react'
import ReactDOM from 'react-dom'
import getUniqueCategories from '../../single_visualization/utils/getUniqueCategories'
import sortCategoryData from '../../single_visualization/utils/sortCategoryData'
import generateBarSeries from '../../single_visualization/data_interfaces/generateBarSeries'
import BarChart from '../../single_visualization/visualization_types/BarChart'
import ResizeObserver from '../../mocks/observer'

import data from '../../../../json/data.json'

jest.mock('../../mocks/observer')

let container
let series
const uniqueCategories = getUniqueCategories(data)
let settings
let chartSpecificOptions
beforeEach(() => {
  container = document.createElement('div')
  document.body.append(container)
  chartSpecificOptions = {
    xAxis: 'DecisionYear',
    yAxis: 'Rapporteur',
    categoriesSelectedX: uniqueCategories['DecisionYear'],
    categoriesSelectedY: uniqueCategories['Rapporteur'],
    stacked: false,
    stackType: false,
    horizontal: false,
  }

  settings = { chartSpecificOptions, data }
  series = generateBarSeries(settings)
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

test('initial render', () => {
  ReactDOM.render(
    <BarChart
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

test('render with stackType of 100%', () => {
  settings.stacked = true
  settings.stackType = true
  ReactDOM.render(
    <BarChart
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

test('render with switched axes', () => {
  settings.horizontal = true
  ReactDOM.render(
    <BarChart
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
