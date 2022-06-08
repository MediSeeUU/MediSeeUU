// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
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
  return { data: Object.values(dict), euNumbers: Object.values(euNumbers) }
}
