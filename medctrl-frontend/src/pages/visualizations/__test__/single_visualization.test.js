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
import SingleVisualization from '../single_visualization/SingleVisualization'
import ResizeObserver from '../mocks/observer'

import data from '../../../testJson/data.json'
import GetUniqueCategories from '../single_visualization/utils/GetUniqueCategories'

jest.mock('../mocks/observer')

let container
let setting
beforeEach(() => {
  container = document.createElement('div')
  document.body.append(container)
  const unique = GetUniqueCategories(data)
  setting = {
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
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

test('render initial single visualization', () => {
  ReactDOM.render(<SingleVisualization id={1} data={data} settings={setting}/>, container)
})

test('export to svg', () => {
  ReactDOM.render(<SingleVisualization id={1} data={data} settings={setting}/>, container)
  fireEvent.click(screen.getByRole('button', { name: 'Export as SVG' }))
})

test('export to png', () => {
  ReactDOM.render(<SingleVisualization id={1} data={data} settings={setting}/>, container)
  fireEvent.click(screen.getByRole('button', { name: 'Export as PNG' }))
})

test('remove itself', () => {
  const onRemoval = jest.fn()
  ReactDOM.render(
    <SingleVisualization id={1} data={data} onRemoval={onRemoval} settings={setting}/>,
    container
  )
  fireEvent.click(screen.getByRole('button', { name: '' }))
})

//render visualisation with line chart
test('render with line chart', () => {
  const unique = GetUniqueCategories(data)
  setting = {
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
  
  ReactDOM.render(<SingleVisualization id={1} data={data} settings={setting}/>, container)
})

//render visualisation with pie chart
test('render with pie chart', () => {
  const unique = GetUniqueCategories(data)
  setting = {
    id: 1,
    chart_type: 'pie',
    chartSpecificOptions: {
      chosenVariables: 'Rapporteur',
      categoriesSelected: [],
    },
    legend_on: true,
    labels_on: false,
    data: data,
    series: [],
    uniqueCategories: unique,
    changeName: '',
  }

  ReactDOM.render(<SingleVisualization id={1} data={data} settings={setting}/>, container)
})