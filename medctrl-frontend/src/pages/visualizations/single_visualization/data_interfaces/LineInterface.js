import sortCategoryData from '../utils/SortCategoryData'

// generates series for a line chart
export default function GenerateLineSeries(options, data) {
  // no categories have been selected
  if (options.chartSpecificOptions.categoriesSelectedX.length === 0) {
    return []
  }
  let xAxis = options.chartSpecificOptions.xAxis
  let yAxis = options.chartSpecificOptions.yAxis
  let categoriesSelectedX = sortCategoryData(
    options.chartSpecificOptions.categoriesSelectedX
  )
  let categoriesSelectedY = sortCategoryData(
    options.chartSpecificOptions.categoriesSelectedY
  )

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
function PollChosenVariable(xAxis, yAxis, categoriesX, categoriesY, data) {
  let dict = {}

  // adding a key for each category
  categoriesX.forEach((category) => {
    dict[category] = {}
  })

  // going through all data entries
  data.forEach((element) => {
    // only if the value of the x/y variable is one of the selected categories
    if (
      categoriesY.includes(element[yAxis]) &&
      categoriesX.includes(element[xAxis])
    ) {
      if (dict[element[xAxis]][element[yAxis]] === undefined) {
        dict[element[xAxis]][element[yAxis]] = 1
      } else {
        dict[element[xAxis]][element[yAxis]] += 1
      }
    }
  })

  return dict
}

// Creates an array for each selected category of the y variable.
// If a y category was never combined with an x category,
// a 0 will be added, otherwise the amount of occurrences is added.
function CreateSelectedSeries(dict, categoriesY, categoriesX) {
  let series = {}
  categoriesY.forEach((category) => {
    series[category] = []
  })

  categoriesX.forEach((k) => {
    categoriesY.forEach((category) => {
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
