import searchData from "./search"
import filterData from "./filter"
import sortData from "./sorting"

// Update the data by applying search, filters and sorters
function updateData(data, search, filters, sorters) {
  let updatedData = [...data]
  updatedData = searchData(updatedData, search)
  updatedData = filterData(updatedData, filters)
  updatedData = sortData(updatedData, sorters)
  return updatedData
}

export default updateData
