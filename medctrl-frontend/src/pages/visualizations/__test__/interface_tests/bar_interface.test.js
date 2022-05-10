import {
  cleanup,
  render,
  fireEvent,
  waitFor,
  screen,
  getByRole,
  getByText,
} from '@testing-library/react'
import GenerateBarSeries from '../../single_visualization/data_interfaces/BarInterface'
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'

import data from '../../../../testJson/data.json'

test('no selected categories', () => {
  const uniqueCategories = GetUniqueCategories(data)
  const options = {
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelected: [],
    },
  }
  const series = GenerateBarSeries(options, uniqueCategories, data)
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
  const series = GenerateBarSeries(options, uniqueCategories, data)
  expect(series).toHaveLength(2)
  expect(series[0].name).toBe('United Kingdom')
  expect(series[1].name).toBe('Denmark')
})

test('data in categories', () => {
  const uniqueCategories = GetUniqueCategories(data)
  const options = {
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelected: ['United Kingdom', 'Denmark'],
    },
  }
  const series = GenerateBarSeries(options, uniqueCategories, data)
  series.forEach((element) => {
    let filteredData = data.filter((datael) => element.eu_numbers.includes(datael.EUNoShort))
    filteredData.forEach((datael) => {
      expect(element.name).toBe(datael.Rapporteur)
    })
  })
})
