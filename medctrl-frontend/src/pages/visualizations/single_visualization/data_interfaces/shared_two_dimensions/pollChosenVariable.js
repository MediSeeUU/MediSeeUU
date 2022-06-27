// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

// Counts the number of occurrences a given value of the x variable is paired
// with a given value of the y variable.
export default function pollChosenVariable(
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
        // 'initializing' the entry
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
