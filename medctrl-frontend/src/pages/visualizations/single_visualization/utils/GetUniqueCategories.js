// takes the (JSON) data and gets the categories for each variable
export default function GetUniqueCategories(data) {
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

  // sorting the array
  for (let categories in dict) {
    dict[categories] = dict[categories].sort(function (a, b) {
      return String(a).localeCompare(String(b), 'en', {
        numeric: true,
        sensitivity: 'base',
      })
   })
  }

  return dict
}