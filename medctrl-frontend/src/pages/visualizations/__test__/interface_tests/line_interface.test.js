import GenerateLineSeries from '../../single_visualization/data_interfaces/LineInterface'
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'

import data from '../../../../json/data.json'

test('no selected y categories', () => {
  const uniqueCategories = GetUniqueCategories(data)
  const options = {
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelectedX: uniqueCategories['DecisionYear'],
      categoriesSelectedY: [],
    },
    data: data,
  }
  const series = GenerateLineSeries(options)
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
    data: data,
  }
  const series = GenerateLineSeries(options)
  expect(series).toHaveLength(2)
  expect(series[0].name).toBe('Denmark')
  expect(series[1].name).toBe('United Kingdom')
})

test('categories in data', () => {
  const uniqueCategories = GetUniqueCategories(data)
  const options = {
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelectedX: uniqueCategories['DecisionYear'],
      categoriesSelectedY: ['United Kingdom', 'Denmark'],
    },
    data: data,
  }
  const series = GenerateLineSeries(options)
  series.forEach((element) => {
    let filteredData = data.filter((datael) =>
      element.euNumbers.flat().includes(datael.EUNoShort)
    )
    filteredData.forEach((datael) => {
      expect(element.name).toBe(datael.Rapporteur)
      expect(
        uniqueCategories['DecisionYear'].includes(
          datael.DecisionYear.toString()
        )
      ).toBe(true)
    })
  })
})
