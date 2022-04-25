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
import GeneratePieSeries from '../../single_visualization/data_interfaces/PieInterface'
import PieChart from '../../single_visualization/visualization_types/PieChart'
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
      chosenVariable: 'Rapporteur',
      categoriesSelected: ['United Kingdom'],
    },
  }
  series = GeneratePieSeries(chartSpecificOptions, data)
  uniqueCategories = GetUniqueCategories(data)
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
      categories={uniqueCategories['Rapporteur']}
      options={{}}
    />,
    container
  )
})
