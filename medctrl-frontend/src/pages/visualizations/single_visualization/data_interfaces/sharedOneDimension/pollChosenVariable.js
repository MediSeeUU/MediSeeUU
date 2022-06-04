// Goes through every data entry,
// if the value of said data entry for the chosen variable
// is one of the chosen categories, its entry in the series will be incremented.
export function pollChosenVariable(data, xAxis, chosenCategories) {
  let dict = {}
  let euNumbers = {}
  chosenCategories.forEach((category) => {
    dict[category] = 0
    euNumbers[category] = []
  })

  data.forEach((element) => {
    if (chosenCategories.includes(element[xAxis])) {
      dict[element[xAxis]] += 1
      euNumbers[element[xAxis]].push(element.EUNoShort)
    }
  })

  return [dict, euNumbers]
}
