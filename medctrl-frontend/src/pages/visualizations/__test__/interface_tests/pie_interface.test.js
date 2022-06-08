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
import GeneratePieSeries from '../../single_visualization/data_interfaces/PieInterface'

import data from '../../../../testJson/data.json'

test('no categories selected', () => {
  const options = {
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: [],
    },
  }
  const series = GeneratePieSeries(options, data)
  expect(series.data).toHaveLength(0)
  expect(series.euNumbers).toHaveLength(0)
})

test('some categories selected (sorted)', () => {
  const options = {
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: ['United Kingdom', 'Denmark'],
    },
  }
  const series = GeneratePieSeries(options, data)
  expect(series.data).toHaveLength(2)
  expect(series.euNumbers).toHaveLength(2)
})

test('categories in data', () => {
  const options = {
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: ['United Kingdom', 'Denmark'],
    },
  }
  const series = GeneratePieSeries(options, data)
  let filteredData = data.filter((element) =>
    series.euNumbers.flat().includes(element.EUNoShort)
  )
  filteredData.forEach((element) => {
    expect(element.Rapporteur).toMatch(/(United Kingdom|Denmark)/i)
  })
})
