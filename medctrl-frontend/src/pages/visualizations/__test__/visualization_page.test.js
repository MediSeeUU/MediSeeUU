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
import {
  SelectedContext,
  VisualsContext,
  VisualsUpdateContext,
} from '../../../shared/contexts/DataContext'
import GetUniqueCategories from '../single_visualization/utils/GetUniqueCategories'

jest.mock('../mocks/observer')

let container
let visuals
let updateVisuals
let unique = GetUniqueCategories(data)
let defaultVisuals = [
  {
    id: 1,
    chartType: 'bar',
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelectedX: unique['DecisionYear'],
      categoriesSelectedY: unique['Rapporteur'],
    },
    legendOn: true,
    labelsOn: false,
    uniqueCategories: unique,
  },
]

function contexts(children, contextData, pvisuals) {
  visuals = pvisuals ?? defaultVisuals
  updateVisuals = (value) => (visuals = value)
  return (
    <SelectedContext.Provider value={contextData}>
      <VisualsContext.Provider value={visuals}>
        <VisualsUpdateContext.Provider value={updateVisuals}>
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
  var page = contexts(<VisualizationPage />, [])
  ReactDOM.render(page, container)
})

test('initial render', () => {
  var page = contexts(<VisualizationPage />, data)
  ReactDOM.render(page, container)
})

// rendering a visualization page and adding a visualization
test('add a visualization', () => {
  var page = contexts(<VisualizationPage />, data)
  ReactDOM.render(page, container)
  fireEvent.click(screen.getByRole('button', { name: /add visualization/i }))
  // we start with 1 visualization and add another
  expect(visuals.length).toEqual(2)
})

// rendering a visualization page, then removing the initial visualization
test('remove a visualization', () => {
  var page = contexts(<VisualizationPage />, data)
  ReactDOM.render(page, container)
  // the removal button is currently the only button with no text
  let target = screen.getByRole('button', { name: '' })
  fireEvent.click(target)
  // initially the page has 1 visualization
  expect(visuals.length).toEqual(0)
})

// update the visual context when rendering the visualization page with bar chart
test('update a visual', () => {
  let page = contexts(<VisualizationPage />, data)

  ReactDOM.render(page, container)

  let t = screen.getByRole('combobox', { name: /visualization type/i })
  fireEvent.change(t, { target: { name: 'chartType', value: 'line' }})
}) 
