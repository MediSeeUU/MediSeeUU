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
let unique = GetUniqueCategories(data)
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
    series: [],
    uniqueCategories: unique,
    key: '',
  }
})

afterEach(() => {
  document.body.removeChild(container)
  container = null
})

test('render initial single visualization', () => {
  ReactDOM.render(
    <SingleVisualization id={1} data={data} settings={setting} />,
    container
  )
})

test('export to svg', () => {
  ReactDOM.render(
    <SingleVisualization id={1} data={data} settings={setting} />,
    container
  )
  fireEvent.click(screen.getByRole('button', { name: 'Export as SVG' }))
})

test('export to png', () => {
  ReactDOM.render(
    <SingleVisualization id={1} data={data} settings={setting} />,
    container
  )
  fireEvent.click(screen.getByRole('button', { name: 'Export as PNG' }))
})

test('remove itself', () => {
  const onRemoval = jest.fn()
  ReactDOM.render(
    <SingleVisualization
      id={1}
      data={data}
      onRemoval={onRemoval}
      settings={setting}
    />,
    container
  )
  fireEvent.click(screen.getByRole('button', { name: '' }))
})

//render visualisation with line chart
test('render with line chart', () => {
  const unique = GetUniqueCategories(data)
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
    series: [],
    uniqueCategories: unique,
    key: '',
  }

  ReactDOM.render(
    <SingleVisualization id={1} data={data} settings={setting} />,
    container
  )
})

//render visualisation with pie chart
test('render with pie chart', () => {
  const unique = GetUniqueCategories(data)
  setting = {
    id: 1,
    chartType: 'pie',
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: unique['Rapporteur'],
    },
    legendOn: true,
    labelsOn: false,
    data: data,
    series: [],
    uniqueCategories: unique,
    key: '',
  }

  ReactDOM.render(
    <SingleVisualization id={1} data={data} settings={setting} />,
    container
  )
})
