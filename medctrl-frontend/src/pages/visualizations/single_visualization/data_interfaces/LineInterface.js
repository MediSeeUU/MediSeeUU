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

  let [dict, eu_numbers] = PollChosenVariable(
    xAxis,
    yAxis,
    categoriesSelectedX,
    categoriesSelectedY,
    data
  )

  let [series, eu_series] = CreateSelectedSeries(
    dict,
    eu_numbers,
    categoriesSelectedY,
    categoriesSelectedX
  )

  let seriesFormatted = ToSeriesFormat(series, eu_series)

  return seriesFormatted
}

// Counts the number of occurrences a given value of the x variable is paired
// with a given value of the y variable.
function PollChosenVariable(xAxis, yAxis, categoriesX, categoriesY, data) {
  let dict = {}
  let eu_numbers = {}

  // adding a key for each category
  categoriesX.forEach((category) => {
    dict[category] = {}
    eu_numbers[category] = {}
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
        eu_numbers[element[xAxis]][element[yAxis]] = [element.EUNoShort]
      } else {
        dict[element[xAxis]][element[yAxis]] += 1
        eu_numbers[element[xAxis]][element[yAxis]].push(element.EUNoShort)
      }
    }
  })

  return [dict, eu_numbers]
}

// Creates an array for each selected category of the y variable.
// If a y category was never combined with an x category,
// a 0 will be added, otherwise the amount of occurrences is added.
function CreateSelectedSeries(dict, eu_numbers, categoriesY, categoriesX) {
  let series = {}
  let eu_series = {}

  categoriesY.forEach((category) => {
    series[category] = []
    eu_series[category] = []
  })

  categoriesX.forEach((k) => {
    categoriesY.forEach((category) => {
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
