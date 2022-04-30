// Filter data based on the given query
function searchData(data, query) {
  let updatedData = [...data]
  updatedData = updatedData.filter(obj => {
    let inText = false
    let vals = Object.values(obj)
    for (const val of vals) {
      if (val.toString().toLowerCase().includes(query.toLowerCase())) {
        inText = true
        break
      }
    }
    return inText
  })
  return updatedData
}

export default searchData
