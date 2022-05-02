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
import SingleVisualization from '../../single_visualization/SingleVisualization'
import HandlePNGExport from '../../single_visualization/exports/HandlePNGExport'
import ApexCharts from 'apexcharts'
import ResizeObserver from '../../mocks/observer'

import data from '../../../../testJson/data.json'
import { generateSeries } from '../../single_visualization/SingleVisualization'
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'

jest.mock('../../mocks/observer')

test('export to png', () => {
  const unique = GetUniqueCategories(data)
  var setting = {
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
  setting.series = generateSeries('bar', setting)

  const root = document.createElement('div')
  const vis = ReactDOM.render(
    <SingleVisualization id={1} data={data} settings={setting} />,
    root
  )
  HandlePNGExport(1, ApexCharts)
})
