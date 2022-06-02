import React from 'react'
import ReactDOM from 'react-dom'
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'
import sortCategoryData from '../../single_visualization/utils/SortCategoryData'
import GenerateBarSeries from '../../single_visualization/data_interfaces/BarInterface'
import BarChart from '../../single_visualization/visualization_types/BarChart'
import ResizeObserver from '../../mocks/observer'

import data from '../../../../testJson/data.json'

jest.mock('../../mocks/observer')

let container
let series
const uniqueCategories = GetUniqueCategories(data)
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
  series = GenerateBarSeries(settings)
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
