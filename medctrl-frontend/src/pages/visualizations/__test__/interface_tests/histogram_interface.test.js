// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
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

test('categories in data', () => {
  const options = {
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: ['United Kingdom', 'Denmark'],
    },
  }
  const series = GenerateHistogramSeries(options, data)
  series.forEach((element) => {
    let filteredData = data.filter((datael) =>
      element.euNumbers.flat().includes(datael.EUNoShort)
    )
    filteredData.forEach((datael) => {
      expect(datael.Rapporteur).toMatch(/(United Kingdom|Denmark)/i)
    })
  })
})
