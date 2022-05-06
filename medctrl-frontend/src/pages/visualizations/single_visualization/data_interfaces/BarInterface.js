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

  let [dict, eu_numbers] = PollChosenVariable(
    xAxis,
    yAxis,
    sortedxAxis,
    categoriesSelectedY,
    data
  )

  let [series, eu_series] = CreateSelectedSeries(
    dict,
    eu_numbers,
    categoriesSelectedY,
    sortedxAxis
  )

  let seriesFormatted = ToSeriesFormat(series, eu_series)

  return seriesFormatted
}

/*
  Expects data to be an array of ob objects, 
	where each object has a value for each variable.
	It builds a dictionary where the keys are the categories of the x variable,
	the values themselves are also dictionaries.
	In this dictionary the keys are categories of the y variable,
	the values are how often this combination of categories happened.
*/
function PollChosenVariable(x_axis, y_axis, categories_x, categories_y, data) {
  let dict = {}
  let eu_numbers = {}

  // adding a key for each category
  categories_x.forEach((category) => {
    dict[category] = {}
    eu_numbers[category] = {}
  })

  // going through all data entries
  data.forEach((element) => {
    // only if the value of the y variable is one of the selecte categories
    if (categories_y.includes(element[y_axis])) {
      if (dict[element[x_axis]][element[y_axis]] === undefined) {
        dict[element[x_axis]][element[y_axis]] = 1
        eu_numbers[element[x_axis]][element[y_axis]] = [element.EUNoShort]
      } else {
        dict[element[x_axis]][element[y_axis]] += 1
        eu_numbers[element[x_axis]][element[y_axis]].push(element.EUNoShort)
      }
    }
  })

  return [dict, eu_numbers]
}

/*
  Creates an array for each selected category of the y variable.
  If a y category was never combined with an x category,
	a 0 will be added, otherwise the amount of occurrences.
*/
function CreateSelectedSeries(dict, eu_numbers, categories_y, categories_x) {
  let series = {}
  let eu_series = {}
  categories_y.forEach((category) => {
    series[category] = []
    eu_series[category] = []
  })

  categories_x.forEach((k) => {
    categories_y.forEach((category) => {
      if (dict[k][category] === undefined) {
        series[category].push(0)
        eu_series[category].push([])
      } else {
        series[category].push(dict[k][category])
        eu_series[category].push(eu_numbers[k][category])
      }
    })
  })

  return [series, eu_series]
}

// turning a dict into the data format accepted by ApexChart
// the entry key becomes the name, the entry value becomes the data
function ToSeriesFormat(dict, eu_series) {
  let series = []
  for (let key in dict) {
    series.push({ name: key, data: dict[key], eu_numbers: eu_series[key] })
  }
  return series
}
