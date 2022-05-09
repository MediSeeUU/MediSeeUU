// Filter data based on the given filters
function filterData(data, filters) {
  let updatedData = [...data]
  filters.forEach((item) => {
    updatedData = applyFilter(updatedData, item)
  })
  return updatedData
}

// Function that applies one filter item to the data
function applyFilter(data, item) {
  if (!item.selected) {
    return data
  }
  return data.filter((obj) => {
    return item.input.some((x) =>
      obj[item.selected].toString().toLowerCase().includes(x.toLowerCase())
    )
  })
}

export default filterData
