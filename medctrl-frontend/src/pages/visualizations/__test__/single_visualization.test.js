// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'
import ReactDOM from 'react-dom'
import { fireEvent, screen } from '@testing-library/react'
import SingleVisualization from '../single_visualization/SingleVisualization'
import ResizeObserver from '../mocks/observer'

import data from '../../../json/data.json'
import getUniqueCategories from '../single_visualization/utils/getUniqueCategories'

jest.mock('../mocks/observer')

let container
let setting
const unique = getUniqueCategories(data)
beforeEach(() => {
  container = document.createElement('div')
  document.body.append(container)
  setting = {
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
    uniqueCategories: unique,
  }
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

test('render initial bar chart', () => {
  ReactDOM.render(<SingleVisualization id={1} settings={setting} />, container)
  const target = screen.getByRole('combobox', { name: /visualization type/i })
  expect(target.value).toBe('bar')
})

test('render line chart', () => {
  setting.chartType = 'line'

  ReactDOM.render(<SingleVisualization id={1} settings={setting} />, container)
})

test('render pie chart', () => {
  setting.chartType = 'pie'

  ReactDOM.render(<SingleVisualization id={1} settings={setting} />, container)
})

test('render histogram chart', () => {
  setting.chartType = 'histogram'

  ReactDOM.render(<SingleVisualization id={1} settings={setting} />, container)
})

test('export to svg', () => {
  // Mocking this function,
  // as Jest does not know it.
  URL.createObjectURL = jest.fn()
  ReactDOM.render(<SingleVisualization id={1} settings={setting} />, container)
  fireEvent.click(screen.getByRole('button', { name: 'Export as SVG' }))
})

test('export to png', () => {
  ReactDOM.render(<SingleVisualization id={1} settings={setting} />, container)
  fireEvent.click(screen.getByRole('button', { name: 'Export as PNG' }))
})

// the actual removal/addition/change logic is (mostly) on page level

test('remove itself', () => {
  const onRemoval = jest.fn()
  ReactDOM.render(
    <SingleVisualization id={1} onRemoval={onRemoval} settings={setting} />,
    container
  )
  fireEvent.click(screen.getByRole('button', { name: '' }))
})

// It does not seem to cover the actual error line,
// because it is already thrown in the generateSeries function.
test('render with incorrect chart type', () => {
  setting.chartType = 'brrr chart'

  expect(() =>
    ReactDOM.render(
      <SingleVisualization id={1} settings={setting} />,
      container
    )
  ).toThrow()
})

test('change title', () => {
  const mock = jest.fn()
  ReactDOM.render(
    <SingleVisualization id={1} onFormChangeFunc={mock} settings={setting} />,
    container
  )
  let target = screen.getByRole('textbox')
  fireEvent.change(target, {
    target: { value: 'example title' },
  })
  expect(target.value).toBe('example title')
})

// does not seem to actually update the value of target...
test('update to line chart', () => {
  const mock = jest.fn()
  ReactDOM.render(
    <SingleVisualization id={1} onFormChangeFunc={mock} settings={setting} />,
    container
  )

  let target = screen.getByRole('combobox', { name: /visualization type/i })
  fireEvent.change(target, {
    target: {
      name: 'chartType',
      value: 'line',
    },
  })
})
