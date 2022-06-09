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
import data from '../../../json/data.json'
import { SelectedContext } from '../../../shared/Contexts/SelectedContext'
import { VisualsContext } from '../../../shared/Contexts/VisualsContext'

jest.mock('../mocks/observer')

let container
const visuals = [
  {
    id: 1,
    chartType: 'bar',
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelectedX: [],
      categoriesSelectedY: [],
    },
    legendOn: true,
    labelsOn: false,
  },
]

function contexts(children, contextData, setVisuals) {
  return (
    <SelectedContext.Provider value={contextData}>
      <VisualsContext.Provider value={{ visuals, setVisuals }}>
        {children}
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
  const page = contexts(<VisualizationPage />, [])
  ReactDOM.render(page, container)
})

test('initial render', () => {
  const page = contexts(<VisualizationPage />, data)
  ReactDOM.render(page, container)
})

// rendering a visualization page and adding a visualization
test('add a visualization', () => {
  const page = contexts(<VisualizationPage />, data, (vis) =>
    expect(vis).toHaveLength(2)
  )
  ReactDOM.render(page, container)
  fireEvent.click(screen.getByRole('button', { name: /add visualization/i }))
})

// rendering a visualization page, then removing the initial visualization
test('remove a visualization', () => {
  const page = contexts(<VisualizationPage />, data, (vis) =>
    expect(vis).toHaveLength(0)
  )
  ReactDOM.render(page, container)
  // the removal button is currently the only button with no text
  let target = screen.getByRole('button', { name: '' })
  fireEvent.click(target)
})

// update the visual context when rendering the visualization page with bar chart
test('update a visual', () => {
  const page = contexts(<VisualizationPage />, data, (vis) =>
    expect(vis[0].chartType).toBe('line')
  )
  ReactDOM.render(page, container)
  let t = screen.getByRole('combobox', { name: /visualization type/i })
  fireEvent.change(t, { target: { name: 'chartType', value: 'line' } })
})
