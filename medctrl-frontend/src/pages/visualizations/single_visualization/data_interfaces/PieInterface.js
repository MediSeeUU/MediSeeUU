import sortCategoryData from '../utils/SortCategoryData'

// creates an array of data for a pie chart
export default function GeneratePieSeries(options, data) {
  let xAxis = options.chartSpecificOptions.xAxis
  let chosenCategories = sortCategoryData(
    options.chartSpecificOptions.categoriesSelectedX
  )
  let pieSeries = CreatePieSeries(data, xAxis, chosenCategories)

  return pieSeries
}

// Goes through every data entry,
// if the value of said data entry for the chosen variable
// is one of the chosen categories, its entry in the series will be incremented.
function CreatePieSeries(data, xAxis, chosenCategories) {
  let dict = {}
  chosenCategories.forEach((category) => {
    dict[category] = 0
  })

  data.forEach((element) => {
    if (chosenCategories.includes(element[xAxis])) {
      dict[element[xAxis]] += 1
    }
  })
  return Object.values(dict)
}
