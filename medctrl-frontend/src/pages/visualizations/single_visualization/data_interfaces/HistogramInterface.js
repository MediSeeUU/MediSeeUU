import sortCategoryData from '../utils/SortCategoryData'
import { pollChosenVariable } from './sharedOneDimension/pollChosenVariable'

// creates an array of data for a Histogram chart
export default function GenerateHistogramSeries(settings) {
  if (settings.chartSpecificsettings.categoriesSelectedX.length === 0) {
    return []
  }
  const xAxis = settings.chartSpecificsettings.xAxis
  const data = settings.data
  const chosenCategories = sortCategoryData(
    settings.chartSpecificsettings.categoriesSelectedX
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
