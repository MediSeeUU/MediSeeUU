import sortCategoryData from '../utils/SortCategoryData'

// creates an array of data for a Histogram chart
export default function GenerateHistogramSeries(options, data) {
  let xAxis = options.chartSpecificOptions.xAxis
  let chosenCategories = sortCategoryData(
    options.chartSpecificOptions.categoriesSelectedX
  )

  let HistogramSeries = CreateHistogramSeries(data, xAxis, chosenCategories)

  return HistogramSeries
}

// Goes through every data entry,
// if the value of said data entry for the chosen variable
// is one of the chosen categories, its entry in the series will be incremented.
function CreateHistogramSeries(data, xAxis, chosenCategories) {
  let dict = {}
  let eu_numbers = {}
  chosenCategories.forEach((category) => {
    dict[category] = 0
    eu_numbers[category] = []
  })

  data.forEach((element) => {
    if (chosenCategories.includes(element[xAxis])) {
      dict[element[xAxis]] += 1
      eu_numbers[element[xAxis]].push(element.EUNoShort)
    }
  })

  return [{ name: 'amount', data: Object.values(dict), eu_numbers: Object.values(eu_numbers) }]
}
