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
import { generateSeries } from '../../single_visualization/utils/GenerateSeries'
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'

jest.mock('../../mocks/observer')

test('export to png', () => {
  const mock = jest.fn()
  const unique = GetUniqueCategories(data)
  var setting = {
    id: 0,
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
  const series = generateSeries('bar', setting)

  const root = document.createElement('div')
  const vis = render(
    <SingleVisualization
      id={0}
      data={data}
      settings={setting}
      keys={[0]}
      series={[series]}
      onDataClick={mock}
    />,
    root
  )
  screen.logTestingPlaygroundURL()
  HandlePNGExport(1, 'example title', ApexCharts)
})
