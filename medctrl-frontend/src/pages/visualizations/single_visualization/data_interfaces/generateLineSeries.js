// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import sortCategoryData from '../utils/sortCategoryData'
import pollChosenVariable from './shared_two_dimensions/pollChosenVariable'
import createSelectedSeries from './shared_two_dimensions/createSelectedSeries'
import toSeriesFormat from './shared_two_dimensions/toSeriesFormat'

// generates series for a line chart
export default function generateLineSeries(settings) {
  // no categories have been selected
  if (
    settings.chartSpecificOptions.categoriesSelectedX.length === 0 ||
    settings.chartSpecificOptions.categoriesSelectedY.length === 0
  ) {
    return []
  }

  const xAxis = settings.chartSpecificOptions.xAxis
  const yAxis = settings.chartSpecificOptions.yAxis
  const data = settings.data

  const categoriesSelectedX = sortCategoryData(
    settings.chartSpecificOptions.categoriesSelectedX
  )
  const categoriesSelectedY = sortCategoryData(
    settings.chartSpecificOptions.categoriesSelectedY
  )

  let [dict, euNumbers] = pollChosenVariable(
    xAxis,
    yAxis,
    categoriesSelectedX,
    categoriesSelectedY,
    data
  )

  let [series, euSeries] = createSelectedSeries(
    dict,
    euNumbers,
    categoriesSelectedY,
    categoriesSelectedX
  )

  let seriesFormatted = toSeriesFormat(series, euSeries)

  return seriesFormatted
}
