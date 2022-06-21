// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import { firstBy } from 'thenby'

// Search data based on the given query by first filtering and then applying a ranking
function searchData(data, query, columns) {
  let updatedData = [...data]
  updatedData = filterData(updatedData, query.toLowerCase().split(' '))
  updatedData = rankData(updatedData, query.toLowerCase(), columns)
  return updatedData
}

// Filter data on query
function filterData(data, query) {
  return data.filter((obj) => {
    // Get a list of all the values in the datapoint and preprocess it by tokenizing
    const vals = Object.values(obj)
      .map((val) => val.toString().toLowerCase().split(' '))
      .flat()
    // Every query term should be occuring somewhere in the values (urls not included)
    return query.every((val1) =>
      vals.some(
        (val2) =>
          !val2.startsWith('http://') &&
          !val2.startsWith('https://') &&
          val2.includes(val1)
      )
    )
  })
}

// Rank data: rank on left-to-right columns and on query occurences in the data
function rankData(data, query, columns) {
  return (
    data
      .map((obj) => {
        // We first determine the ranking
        let rank = columns.length
        for (let i = 0; i < columns.length; i++) {
          let objVal = obj[columns[i]].toString().toLowerCase()
          if (objVal.includes(query)) {
            // If the value is equal to the query, then we should rank this high
            if (objVal === query) {
              rank = -1
            }
            // Otherwise the ranking is the first matching column
            else {
              rank = i
            }
            break
          }
        }
        // Then we determine the amount of query occurences
        let count = 0
        let vals = Object.values(obj)
        for (const val of vals) {
          if (val.toString().toLowerCase().includes(query)) {
            count++
          }
        }
        // This will be returned in the object data
        return { data: obj, rank: rank, count: count }
      })
      // Then we first sort on rank and then on amount of occurences
      .sort(
        firstBy((a, b) => a.rank - b.rank).thenBy((a, b) => b.count - a.count)
      )
      // These properties will then again be deleted from the object after sorting
      .map((obj) => {
        return obj.data
      })
  )
}

export default searchData
