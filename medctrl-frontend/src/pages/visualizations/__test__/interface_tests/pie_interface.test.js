import {
  cleanup,
  render,
  fireEvent,
  waitFor,
  screen,
  getByRole,
  getByText,
} from '@testing-library/react'
import GeneratePieSeries from '../../single_visualization/data_interfaces/PieInterface'

import data from '../../../../testJson/data.json'

test('no data', () => {
  const options = {
    chartSpecificOptions: {
      chosenVariable: 'Rapporteur',
      categoriesSelected: [],
    },
  }
  const series = GeneratePieSeries(options, data)
  expect(series.length).toBe(0)
})

test('some categories selected', () => {
  const options = {
    chartSpecificOptions: {
      chosenVariable: 'Rapporteur',
      categoriesSelected: ['United Kingdom', 'Denmark'],
    },
  }
  const series = GeneratePieSeries(options, data)
  expect(series).toHaveLength(2)
})
