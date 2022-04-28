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
import VisualizationPage from '../VisualizationPage'
import ResizeObserver from '../mocks/observer'

import data from '../../../testJson/data.json'
import { SelectedContext, VisualsContext, VisualsUpdateContext } from '../../../shared/contexts/DataContext'
import GetUniqueCategories from '../single_visualization/utils/GetUniqueCategories'
import { generateSeries } from '../single_visualization/SingleVisualization'

jest.mock('../mocks/observer')

let container
let visuals
function contexts(children, contextData) {
  var unique = GetUniqueCategories(data)
  visuals = [{
    id: 1,
    chart_type: 'bar',
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelected: [],
    },
    legend_on: true,
    labels_on: false,
    data: data,
    series: [],
    uniqueCategories: unique,
    changeName: '',
  }
  ]
  if (contextData.length <= 0){
    visuals = []
  } else {
    visuals[0].series = generateSeries(visuals[0].chart_type, visuals[0])
  }
  return (
    <SelectedContext.Provider value={contextData}>
      <VisualsContext.Provider value={visuals}>
        <VisualsUpdateContext.Provider value={(value) => visuals = value}>
          {children}
        </VisualsUpdateContext.Provider>
      </VisualsContext.Provider>
    </SelectedContext.Provider>
  )
}
beforeEach(() => {
  container = document.createElement('div')
  document.body.append(container)
  
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

test('no data', () => {
  var page = contexts(<VisualizationPage/>, [])
  ReactDOM.render(page, container)
})

test('initial render', () => {
  var page = contexts(<VisualizationPage/>, data)
  ReactDOM.render(page, container)
})

// rendering a visualization page and adding a visualization
test('add a visualization', () => {
  var page = contexts(<VisualizationPage/>, data)
  ReactDOM.render(page, container)
  fireEvent.click(screen.getByRole('button', { name: /add visualization/i }))
  // we start with 1 visualization and add another
  expect(visuals.length).toEqual(2)
})

// rendering a visualization page, then removing the initial visualization
test('remove a visualization', () => {
  var page = contexts(<VisualizationPage/>, data)
  ReactDOM.render(page, container)
  // the removal button is currently the only button with no text
  let target = screen.getByRole('button', { name: '' })
  // it throws an error that has to do with the ApexCharts library,
  // we have not found any way around this sadly
  fireEvent.click(target)
  expect(visuals.length).toEqual(0)
})
