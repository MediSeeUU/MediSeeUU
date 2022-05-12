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
import HandleSVGExport from '../../single_visualization/exports/HandleSVGExport'
import ApexCharts from 'apexcharts'
import ResizeObserver from '../../mocks/observer'

import data from '../../../../testJson/data.json'
import { generateSeries } from '../../single_visualization/SingleVisualization'
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'

jest.mock('../../mocks/observer')

test('export to svg', () => {
  const unique = GetUniqueCategories(data)
  var setting = {
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
  setting.series = generateSeries('bar', setting)

  const root = document.createElement('div')
  ReactDOM.render(
    <SingleVisualization id={1} data={data} settings={setting} />,
    root
  )
  HandleSVGExport(1, 'example title', ApexCharts)
})
