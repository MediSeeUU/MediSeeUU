// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
// Takes the (JSON) data and gets the categories for each variable.
// For example, the data set of [1,2,2,3] has the unique categories 1, 2 and 3.
export default function getUniqueCategories(data) {
  let dict = {}

  // element is a single 'database entry'
  data.forEach((element) => {
    for (let attribute in element) {
      let val = element[attribute]
      if (dict[attribute] === undefined) {
        dict[attribute] = [val]
      } else {
        if (!dict[attribute].includes(val)) {
          dict[attribute].push(val)
        }
      }
    }
  })
  return dict
}
