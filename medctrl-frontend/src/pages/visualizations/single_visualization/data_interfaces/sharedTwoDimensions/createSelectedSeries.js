// Creates an array for each selected category of the y variable.
// If a y category was never combined with an x category,
// a 0 will be added, otherwise the amount of occurrences is added.
export function createSelectedSeries(
  dict,
  euNumbers,
  categoriesSelectedY,
  categoriesSelectedX
) {
  let series = {}
  let euSeries = {}

  categoriesSelectedY.forEach((category) => {
    series[category] = []
    euSeries[category] = []
  })

  categoriesSelectedX.forEach((k) => {
    categoriesSelectedY.forEach((category) => {
      if (dict[k][category] === undefined) {
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
