// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import sortCategoryData from '../utils/sortCategoryData'
import pollChosenVariable from './shared_one_dimension/pollChosenVariable'

// creates an array of data for a timeline chart
export default function generateTimelineSeries(settings) {
  // no categories have been selected
  if (settings.chartSpecificOptions.categoriesSelectedX.length === 0) {
    return { data: [], eu_pnumbers: [] }
  }

  const xAxis = settings.chartSpecificOptions.xAxis
  const data = settings.data

  const chosenCategories = sortCategoryData(
    settings.chartSpecificOptions.categoriesSelectedX
  )

  let [dict, eu_pnumbers] = pollChosenVariable(data, xAxis, chosenCategories)

  return { data: Object.values(dict), eu_pnumbers: Object.values(eu_pnumbers) }
}
