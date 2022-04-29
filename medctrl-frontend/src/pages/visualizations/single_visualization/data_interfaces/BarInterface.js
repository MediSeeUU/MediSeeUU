import sortCategoryData from '../utils/SortCategoryData'

/* 
  generates series for a bar chart,
  keep in mind that the index of a serie corresponds with the index of the 
  'xaxis: {categories}' option!  
*/
export default function GenerateBarSeries(options, allCategories, data) {
  let xAxis = options.chartSpecificOptions.xAxis
  let yAxis = options.chartSpecificOptions.yAxis
  let categoriesSelectedY = options.chartSpecificOptions.categoriesSelected
  let sortedxAxis = sortCategoryData(allCategories[xAxis])

  let dict = PollChosenVariable(
    xAxis,
    yAxis,
    sortedxAxis,
    categoriesSelectedY,
    data
  )

  let series = CreateSelectedSeries(dict, categoriesSelectedY, sortedxAxis)

  let seriesFormatted = ToSeriesFormat(series)

  return seriesFormatted
}

/*
  Expects data to be an array of of objects, 
	where each object has a value for each variable.
	It builds a dictionary where the keys are the categories of the x variable,
	the values themselves are also dictionaries.
	In this dictionary the keys are categories of the y variable,
	the values are how often this combination of categories happened.
*/
function PollChosenVariable(x_axis, y_axis, categories_x, categories_y, data) {
  let dict = {}

  // adding a key for each category
  categories_x.forEach((category) => {
    dict[category] = {}
  })

  // going through all data entries
  data.forEach((element) => {
    // only if the value of the y variable is one of the selected categories
    if (categories_y.includes(element[y_axis])) {
      if (dict[element[x_axis]][element[y_axis]] === undefined) {
        dict[element[x_axis]][element[y_axis]] = 1
      } else {
        dict[element[x_axis]][element[y_axis]] += 1
      }
    }
  })

  return dict
}

/*
  Creates an array for each selected category of the y variable.
  If a y category was never combined with an x category,
	a 0 will be added, otherwise the amount of occurrences.
*/
function CreateSelectedSeries(dict, categories_y, categories_x) {
  let series = {}
  categories_y.forEach((category) => {
    series[category] = []
  })

  categories_x.forEach((k) => {
    categories_y.forEach((category) => {
      if (dict[k][category] === undefined) {
        series[category].push(0)
      } else {
        series[category].push(dict[k][category])
      }
    })
  })

  return series
}

// turning a dict into the data format accepted by ApexChart
// the entry key becomes the name, the entry value becomes the data
function ToSeriesFormat(dict) {
  let series = []
  for (let key in dict) {
    series.push({ name: key, data: dict[key] })
  }
  return series
}
