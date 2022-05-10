import {
  cleanup,
  render,
  fireEvent,
  waitFor,
  screen,
  getByRole,
  getByText,
} from '@testing-library/react'
import GenerateHistogramSeries from '../../single_visualization/data_interfaces/HistogramInterface'

import data from '../../../../testJson/data.json'

test('no categories selected', () => {
  const options = {
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: [],
    },
  }
  const series = GenerateHistogramSeries(options, data)
  expect(series[0].data.length).toBe(0)
})

test('some categories selected (sorted)', () => {
  const options = {
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: ['United Kingdom', 'Denmark'],
    },
  }
  const series = GenerateHistogramSeries(options, data)
  expect(series[0].data.length).toBe(2)
})
