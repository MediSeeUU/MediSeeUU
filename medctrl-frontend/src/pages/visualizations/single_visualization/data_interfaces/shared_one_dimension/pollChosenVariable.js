// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

// Goes through every data entry,
// if the value of said data entry for the chosen variable is one of the chosen categories,
// its entry in the series will be incremented.
export default function pollChosenVariable(data, xAxis, chosenCategories) {
  let dict = {}
  let euNumbers = {}

  // adding a key for every category
  chosenCategories.forEach((category) => {
    dict[category] = 0
    euNumbers[category] = []
  })

  // incrementing to the matching category
  data.forEach((element) => {
    if (chosenCategories.includes(element[xAxis])) {
      dict[element[xAxis]] += 1
      euNumbers[element[xAxis]].push(element.eunumber)
    }
  })

  return [dict, euNumbers]
}
