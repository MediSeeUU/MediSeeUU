// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import generateBarSeries from '../../single_visualization/data_interfaces/generateBarSeries'
import getUniqueCategories from '../../single_visualization/utils/getUniqueCategories'

import data from '../../../../json/data.json'

test('no selected y categories', () => {
  const uniqueCategories = getUniqueCategories(data)
  const options = {
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelectedX: uniqueCategories['DecisionYear'],
      categoriesSelectedY: [],
    },
    data: data,
  }
  const series = generateBarSeries(options)
  expect(series).toHaveLength(0)
})

test('some selected categories (sorted)', () => {
  const uniqueCategories = getUniqueCategories(data)
  const options = {
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelectedX: uniqueCategories['DecisionYear'],
      categoriesSelectedY: ['United Kingdom', 'Denmark'],
    },
    data: data,
  }
  const series = generateBarSeries(options)
  expect(series).toHaveLength(2)
  expect(series[0].name).toBe('Denmark')
  expect(series[1].name).toBe('United Kingdom')
})

test('categories in data', () => {
  const uniqueCategories = getUniqueCategories(data)
  const options = {
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelectedX: uniqueCategories['DecisionYear'],
      categoriesSelectedY: ['United Kingdom', 'Denmark'],
    },
    data: data,
  }
  const series = generateBarSeries(options)
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
