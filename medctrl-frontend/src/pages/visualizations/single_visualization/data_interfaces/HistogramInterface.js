import sortCategoryData from '../utils/SortCategoryData'
import { pollChosenVariable } from './sharedOneDimension/pollChosenVariable'

// creates an array of data for a Histogram chart
export default function GenerateHistogramSeries(options) {
  const xAxis = options.chartSpecificOptions.xAxis
  const data = options.data
  const chosenCategories = sortCategoryData(
    options.chartSpecificOptions.categoriesSelectedX
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
