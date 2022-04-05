/*
  Creates an array of data for a pie chart.
	Keep in mind that the index of the array corresponds with the index of
  labels/this.props.categories of Pie/DonutChart
*/
export default function GeneratePieSeries(options, allCategories, data) {
  let chosenVariable = options.chartSpecificOptions.chosenVariable
  let chosenCategories = options.chartSpecificOptions.categoriesSelected

  let pieSeries = CreatePieSeries(data, chosenVariable, chosenCategories)

  return pieSeries
}

/* 
  Goes through every data entry,
	if the value of said data entry for the chosen variable
	is one of the chosen categories, its entry in the series will be incremented.
*/
function CreatePieSeries(data, chosenVariable, chosenCategories) {
  let dict = {}
  chosenCategories.forEach((category) => {
    dict[category] = 0
  })

  data.forEach((element) => {
    if (chosenCategories.includes(element[chosenVariable])) {
      dict[element[chosenVariable]] += 1
    }
  })

  return Object.values(dict)
}
