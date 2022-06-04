// Counts the number of occurrences a given value of the x variable is paired
// with a given value of the y variable.
export function pollChosenVariable(
  xAxis,
  yAxis,
  categoriesSelectedX,
  categoriesSelectedY,
  data
) {
  let dict = {}
  let euNumbers = {}

  // adding a key for each category
  categoriesSelectedX.forEach((category) => {
    dict[category] = {}
    euNumbers[category] = {}
  })

  // going through all data entries
  data.forEach((element) => {
    // only if the value of the x/y variable is one of the selected categories
    if (
      categoriesSelectedY.includes(element[yAxis]) &&
      categoriesSelectedX.includes(element[xAxis])
    ) {
      if (dict[element[xAxis]][element[yAxis]] === undefined) {
        dict[element[xAxis]][element[yAxis]] = 1
        euNumbers[element[xAxis]][element[yAxis]] = [element.EUNoShort]
      } else {
        dict[element[xAxis]][element[yAxis]] += 1
        euNumbers[element[xAxis]][element[yAxis]].push(element.EUNoShort)
      }
    }
  })

  return [dict, euNumbers]
}
