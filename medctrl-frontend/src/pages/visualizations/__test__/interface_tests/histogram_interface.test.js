// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import generateHistogramSeries from '../../single_visualization/data_interfaces/generateHistogramSeries'
import data from '../../../../json/data.json'

test('no categories selected', () => {
  const options = {
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: [],
    },
    data: data,
  }
  const series = generateHistogramSeries(options, data)
  expect(series.length).toBe(0)
})

test('some categories selected (sorted)', () => {
  const options = {
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: ['United Kingdom', 'Denmark'],
    },
    data: data,
  }
  const series = generateHistogramSeries(options, data)
  expect(series[0].data.length).toBe(2)
})

test('categories in data', () => {
  const options = {
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: ['United Kingdom', 'Denmark'],
    },
    data: data,
  }
  const series = generateHistogramSeries(options, data)
  series.forEach((element) => {
    let filteredData = data.filter((datael) =>
      element.eu_pnumbers.flat().includes(datael.eu_pnumber)
    )
    filteredData.forEach((datael) => {
      expect(datael.Rapporteur).toMatch(/(United Kingdom|Denmark)/i)
    })
  })
})
