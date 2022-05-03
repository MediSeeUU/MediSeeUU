/*
  Creates an array of data for a Histogram chart.
	Keep in mind that the index of the array corresponds with the index of
  labels/this.props.categories of Histogram
*/
export default function GenerateHistogramSeries(options, data) {
  let chosenVariable = options.chartSpecificOptions.chosenVariable
  let chosenCategories = options.chartSpecificOptions.categoriesSelectedX

  let HistogramSeries = CreateHistogramSeries(
    data,
    chosenVariable,
    chosenCategories
  )

  return HistogramSeries
}

/* 
  Goes through every data entry,
	if the value of said data entry for the chosen variable
	is one of the chosen categories, its entry in the series will be incremented.
*/
function CreateHistogramSeries(data, chosenVariable, chosenCategories) {
  let dict = {}
  chosenCategories.forEach((category) => {
    dict[category] = 0
  })

  data.forEach((element) => {
    if (chosenCategories.includes(element[chosenVariable])) {
      dict[element[chosenVariable]] += 1
    }
  })

  return [{ name: 'categories', data: Object.values(dict) }]
}
