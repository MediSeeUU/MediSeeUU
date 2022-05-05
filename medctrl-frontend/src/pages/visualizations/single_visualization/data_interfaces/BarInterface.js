import sortCategoryData from '../utils/SortCategoryData'

// Generates series for a bar chart
export default function GenerateBarSeries(options, data) {
  // no categories have been selected
  if (options.chartSpecificOptions.categoriesSelectedX.length === 0) {
    return []
  }
  let xAxis = options.chartSpecificOptions.xAxis
  let yAxis = options.chartSpecificOptions.yAxis
  let categoriesSelectedX = sortCategoryData(
    options.chartSpecificOptions.categoriesSelectedX
  )
  let categoriesSelectedY = options.chartSpecificOptions.categoriesSelectedY

  let dict = PollChosenVariable(
    xAxis,
    yAxis,
    categoriesSelectedX,
    categoriesSelectedY,
    data
  )

  let series = CreateSelectedSeries(
    dict,
    categoriesSelectedY,
    categoriesSelectedX
  )

  let seriesFormatted = ToSeriesFormat(series)

  return seriesFormatted
}

// Counts the number of occurrences a given value of the x variable is paired
// with a given value of the y variable.
function PollChosenVariable(x_axis, y_axis, categories_x, categories_y, data) {
  let dict = {}

  // adding a key for each category
  categories_x.forEach((category) => {
    dict[category] = {}
  })

  // going through all data entries
  data.forEach((element) => {
    // only if the value of the x/y variable is one of the selected categories
    if (
      categories_y.includes(element[y_axis]) &&
      categories_x.includes(element[x_axis])
    ) {
      if (dict[element[x_axis]][element[y_axis]] === undefined) {
        dict[element[x_axis]][element[y_axis]] = 1
      } else {
        dict[element[x_axis]][element[y_axis]] += 1
      }
    }
  })

  return dict
}

// Creates an array for each selected category of the y variable.
// If a y category was never combined with an x category,
// a 0 will be added, otherwise the amount of occurrences is added.
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
