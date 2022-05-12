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

test('no selected y categories', () => {
  const uniqueCategories = GetUniqueCategories(data)
  const options = {
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelectedX: uniqueCategories['DecisionYear'],
      categoriesSelectedY: [],
    },
  }
  const series = GenerateLineSeries(options, data)
  expect(series).toHaveLength(0)
})

test('some selected categories (sorted)', () => {
  const uniqueCategories = GetUniqueCategories(data)
  const options = {
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelectedX: uniqueCategories['DecisionYear'],
      categoriesSelectedY: ['United Kingdom', 'Denmark'],
    },
  }
  const series = GenerateLineSeries(options, data)
  expect(series).toHaveLength(2)
  expect(series[0].name).toBe('Denmark')
})
