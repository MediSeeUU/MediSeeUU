import GenerateHistogramSeries from '../../single_visualization/data_interfaces/generateHistogramSeries'

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
      element.euNumbers.flat().includes(datael.EUNoShort)
    )
    filteredData.forEach((datael) => {
      expect(datael.Rapporteur).toMatch(/(United Kingdom|Denmark)/i)
    })
  })
})
