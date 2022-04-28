import {
  cleanup,
  render,
  fireEvent,
  waitFor,
  screen,
  getByRole,
  getByText,
} from '@testing-library/react'
import GenerateLineSeries from '../../single_visualization/data_interfaces/LineInterface'
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'

import data from '../../../../testJson/data.json'

test('no data', () => {
  const uniqueCategories = GetUniqueCategories(data)
  const options = {
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelected: [],
    },
  }
  const series = GenerateLineSeries(options, uniqueCategories, data)
  expect(series).toHaveLength(0)
})

test('some selected categories', () => {
  const uniqueCategories = GetUniqueCategories(data)
  const options = {
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelected: ['United Kingdom', 'Denmark'],
    },
  }
  const series = GenerateLineSeries(options, uniqueCategories, data)
  expect(series).toHaveLength(2)
  expect(series[0].name).toBe('United Kingdom')
})
