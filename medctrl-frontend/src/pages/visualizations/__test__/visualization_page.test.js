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
import { generateSeries } from '../single_visualization/SingleVisualization'

jest.mock('../mocks/observer')

let container
let visuals
let updateVisuals
let unique = GetUniqueCategories(data)
function contexts(children, contextData) {
  visuals = [
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
      data: data,
      series: [],
      uniqueCategories: unique,
      changeName: '',
    },
  ]
  if (contextData.length <= 0) {
    visuals = []
  } else {
    visuals[0].series = generateSeries(visuals[0].chartType, visuals[0])
  }
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
  // it throws an error that has to do with the ApexCharts library,
  // we have not found any way around this sadly
  fireEvent.click(target)
  expect(visuals.length).toEqual(0)
})

// update the visual context when rendering the visualization page with bar chart
test('update visuals when rendering with bar', () => {
  visuals = [
    {
      id: 1,
      chartType: 'bar',
      chartSpecificOptions: {
        xAxis: 'DecisionYear',
        yAxis: 'Rapporteur',
        categoriesSelectedX: ['1995', '1996'],
        categoriesSelectedY: unique['Rapporteur'],
      },
      legendOn: true,
      labelsOn: false,
      data: [],
      series: [],
      uniqueCategories: [],
      changeName: '',
    },
  ]
  const page = (
    <SelectedContext.Provider value={data}>
      <VisualsContext.Provider value={visuals}>
        <VisualsUpdateContext.Provider value={(value) => (visuals = value)}>
          <VisualizationPage />
        </VisualsUpdateContext.Provider>
      </VisualsContext.Provider>
    </SelectedContext.Provider>
  )

  ReactDOM.render(page, container)
  //check variable length in visuals
  expect(visuals[0].data.length).not.toEqual(0)
  expect(visuals[0].series.length).not.toEqual(0)
  expect(visuals[0].uniqueCategories.length).not.toEqual(0)
})

// update the visual context when rendering the visualization page with line chart
test('update visuals when rendering with line', () => {
  visuals = [
    {
      id: 1,
      chartType: 'line',
      chartSpecificOptions: {
        xAxis: 'DecisionYear',
        yAxis: 'Rapporteur',
        categoriesSelectedX: ['1995', '1996'],
        categoriesSelectedY: unique['Rapporteur'],
      },
      legendOn: true,
      labelsOn: false,
      data: [],
      series: [],
      uniqueCategories: [],
      changeName: '',
    },
  ]
  const page = (
    <SelectedContext.Provider value={data}>
      <VisualsContext.Provider value={visuals}>
        <VisualsUpdateContext.Provider value={(value) => (visuals = value)}>
          <VisualizationPage />
        </VisualsUpdateContext.Provider>
      </VisualsContext.Provider>
    </SelectedContext.Provider>
  )

  ReactDOM.render(page, container)
  //check variable length in visuals
  expect(visuals[0].data.length).not.toEqual(0)
  expect(visuals[0].series.length).not.toEqual(0)
  expect(visuals[0].uniqueCategories.length).not.toEqual(0)
})

// update the visual context when rendering the visualization page with pie chart
test('update visuals when rendering with pie', () => {
  visuals = [
    {
      id: 1,
      chartType: 'pie',
      chartSpecificOptions: {
        xAxis: 'Rapporteur',
        categoriesSelectedX: unique['Rapporteur'],
      },
      legendOn: true,
      labelsOn: false,
      data: [],
      series: [],
      uniqueCategories: [],
      changeName: '',
    },
  ]
  const page = (
    <SelectedContext.Provider value={data}>
      <VisualsContext.Provider value={visuals}>
        <VisualsUpdateContext.Provider value={(value) => (visuals = value)}>
          <VisualizationPage />
        </VisualsUpdateContext.Provider>
      </VisualsContext.Provider>
    </SelectedContext.Provider>
  )

  ReactDOM.render(page, container)
  //check variable length in visuals
  expect(visuals[0].data.length).not.toEqual(0)
  expect(visuals[0].series.length).not.toEqual(0)
  expect(visuals[0].uniqueCategories.length).not.toEqual(0)
})
