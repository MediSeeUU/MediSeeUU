/*
  Expects data to be an array of ob objects, 
	where each object has a value for each variable.
	It builds a dictionary where the keys are the categories of the x variable,
	the values themselves are also dictionaries.
	In this dictionary the keys are categories of the y variable,
	the values are how often this combination of categories happened.
*/
export function PollChosenVariable(
  x_axis,
  y_axis,
  categories_x,
  categories_y,
  data
) {
  let dict = {}

  // adding a key for each category
  categories_x.forEach((category) => {
    dict[category] = {}
  })

  // going through all data entries
  data.forEach((element) => {
    // only if the value of the y variable is one of the selecte categories
    if (categories_y.includes(element[y_axis])) {
      if (dict[element[x_axis]][element[y_axis]] === undefined) {
        dict[element[x_axis]][element[y_axis]] = 1
      } else {
        dict[element[x_axis]][element[y_axis]] += 1
      }
    }
  })

  return dict
}

/*
  Creates an array for each selected category of the y variable.
  If a y category was never combined with an x category,
	a 0 will be added, otherwise the amount of occurrences.
*/
export function CreateSelectedSeries(dict, categories_y, categories_x) {
  let series = {}
  categories_y.forEach((category) => {
    series[category] = []
  })

	/* 
	  Sorts the keys, so the order corresponds with the categories,
	  given to the BarChart object.
	*/
  let keys = categories_x.sort()

  keys.forEach((k) => {
    categories_y.forEach((category) => {
      if (dict[k][category] === undefined) {
        series[category].push(0)
      } else {
        series[category].push(dict[k][category])
      }
    })
  })

  return series
}
