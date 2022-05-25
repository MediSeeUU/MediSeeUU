import sortCategoryData from '../utils/SortCategoryData'

// creates an array of data for a Histogram chart
export default function GenerateHistogramSeries(options) {
  const xAxis = options.chartSpecificOptions.xAxis
  const data = options.data
  const chosenCategories = sortCategoryData(
    options.chartSpecificOptions.categoriesSelectedX
  )

  const histogramSeries = createHistogramSeries(data, xAxis, chosenCategories)

  return histogramSeries
}

// Goes through every data entry,
// if the value of said data entry for the chosen variable
// is one of the chosen categories, its entry in the series will be incremented.
function createHistogramSeries(data, xAxis, chosenCategories) {
  let dict = {}
  let euNumbers = {}
  chosenCategories.forEach((category) => {
    dict[category] = 0
    euNumbers[category] = []
  })

  data.forEach((element) => {
    if (chosenCategories.includes(element[xAxis])) {
      dict[element[xAxis]] += 1
      euNumbers[element[xAxis]].push(element.EUNoShort)
    }
  })

  return [
    {
      name: 'number',
      data: Object.values(dict),
      euNumbers: Object.values(euNumbers),
    },
  ]
}
