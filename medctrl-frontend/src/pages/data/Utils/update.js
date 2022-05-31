import searchData from './search'
import filterData from './filter'
import sortData from './sorting'

// Update the data by applying search, filters and sorters
function updateData(data, utils, columns) {
  let updatedData = [...data]
  updatedData = searchData(updatedData, utils.search, columns)
  updatedData = filterData(updatedData, utils.filters)
  updatedData = sortData(updatedData, [...utils.sorters])
  return updatedData
}

export default updateData
