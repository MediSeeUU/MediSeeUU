// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import sortCategoryData from '../utils/sortCategoryData'
import pollChosenVariable from './sharedOneDimension/pollChosenVariable'

// creates an array of data for a Histogram chart
export default function generateHistogramSeries(settings) {
  // no categories have been selected
  if (settings.chartSpecificOptions.categoriesSelectedX.length === 0) {
    return []
  }

  const xAxis = settings.chartSpecificOptions.xAxis
  const data = settings.data

  const chosenCategories = sortCategoryData(
    settings.chartSpecificOptions.categoriesSelectedX
  )

  let [dict, euNumbers] = pollChosenVariable(data, xAxis, chosenCategories)

  return [
    {
      name: 'number',
      data: Object.values(dict),
      euNumbers: Object.values(euNumbers),
    },
  ]
}
