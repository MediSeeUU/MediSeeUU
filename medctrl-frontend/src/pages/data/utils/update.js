// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
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
