// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
// Creates an array for each selected category of the y variable.
// If a y category was never combined with an x category,
// a 0 will be added, otherwise the amount of occurrences is added.
export default function createSelectedSeries(
  dict,
  euNumbers,
  categoriesSelectedY,
  categoriesSelectedX
) {
  let series = {}
  let euSeries = {}

  // adding a key for every category
  categoriesSelectedY.forEach((category) => {
    series[category] = []
    euSeries[category] = []
  })

  categoriesSelectedX.forEach((k) => {
    categoriesSelectedY.forEach((category) => {
      if (dict[k][category] === undefined) {
        // the categories for the x and y variable were never matched
        series[category].push(0)
        euSeries[category].push([])
      } else {
        series[category].push(dict[k][category])
        euSeries[category].push(euNumbers[k][category])
      }
    })
  })

  return [series, euSeries]
}
