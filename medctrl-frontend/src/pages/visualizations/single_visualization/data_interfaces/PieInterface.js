import sortCategoryData from '../utils/SortCategoryData'
import { pollChosenVariable } from './sharedOneDimension/pollChosenVariable'

// creates an array of data for a pie chart
export default function GeneratePieSeries(settings) {
  if (settings.chartSpecificOptions.categoriesSelectedX.length === 0) {
    return { data: [], euNumbers: [] }
  }
  const xAxis = settings.chartSpecificOptions.xAxis
  const data = settings.data
  const chosenCategories = sortCategoryData(
    settings.chartSpecificOptions.categoriesSelectedX
  )

  let [dict, euNumbers] = pollChosenVariable(data, xAxis, chosenCategories)

  return { data: Object.values(dict), euNumbers: Object.values(euNumbers) }
}
