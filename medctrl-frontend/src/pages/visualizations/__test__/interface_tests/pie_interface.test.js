import generatePieSeries from '../../single_visualization/data_interfaces/generatePieSeries'

import data from '../../../../json/data.json'

test('no categories selected', () => {
  const options = {
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: [],
    },
    data: data,
  }
  const series = generatePieSeries(options)
  expect(series.data).toHaveLength(0)
  expect(series.euNumbers).toHaveLength(0)
})

test('some categories selected', () => {
  const options = {
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: ['United Kingdom', 'Denmark'],
    },
    data: data,
  }
  const series = generatePieSeries(options)
  expect(series.data).toHaveLength(2)
  expect(series.euNumbers).toHaveLength(2)
})

test('categories in data', () => {
  const options = {
    chartSpecificOptions: {
      xAxis: 'Rapporteur',
      categoriesSelectedX: ['United Kingdom', 'Denmark'],
    },
    data: data,
  }
  const series = generatePieSeries(options)
  let filteredData = data.filter((element) =>
    series.euNumbers.flat().includes(element.EUNoShort)
  )
  filteredData.forEach((element) => {
    expect(element.Rapporteur).toMatch(/(United Kingdom|Denmark)/i)
  })
})
