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
import HandleSVGExport from '../single_visualization/exports/HandleSVGExport'
import ApexCharts from 'apexcharts'
import ResizeObserver from '../mocks/observer'

import data from '../data.json'

jest.mock('../mocks/observer')

test('export to svg', () => {
  render(<SingleVisualization id={1} data={data} />)
  HandleSVGExport(1, ApexCharts)
})
