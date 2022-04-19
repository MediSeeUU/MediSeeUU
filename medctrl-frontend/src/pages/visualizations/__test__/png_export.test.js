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
import HandlePNGExport from '../single_visualization/exports/HandlePNGExport'
import ApexCharts from 'apexcharts'
import ResizeObserver from '../mocks/observer'
import { SelectedContext } from '../../../shared/contexts/DataContext'

import data from '../data.json'

jest.mock('../mocks/observer')

test('export to png', () => {
  render(
    <SelectedContext.Provider value={data}>
      <SingleVisualization id={1} data={data} />
    </SelectedContext.Provider>
  )
  HandlePNGExport(1, ApexCharts)
})
