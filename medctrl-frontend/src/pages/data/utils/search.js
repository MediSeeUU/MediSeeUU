import { firstBy } from 'thenby'

// Search data based on the given query by first filtering and then applying a ranking
function searchData(data, query, columns) {
  let updatedData = [...data]
  updatedData = filterData(updatedData, query.toLowerCase())
  updatedData = rankData(updatedData, query.toLowerCase(), columns)
  return updatedData
}

// Filter data on query
function filterData(data, query) {
  return data.filter((obj) => {
    let inText = false
    let vals = Object.values(obj)
    for (const val of vals) {
      const formattedVal = val.toString().toLowerCase()
      // Query must be included in the table value and not in a url
      if (formattedVal.includes(query) && !formattedVal.startsWith('http')) {
        inText = true
        break
      }
    }
    return inText
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
        return { ...obj, rank: rank, count: count }
      })
      // Then we first sort on rank and then on amount of occurences
      .sort(
        firstBy((a, b) => a.rank - b.rank).thenBy((a, b) => b.count - a.count)
      )
      // These properties will then again be deleted from the object after sorting
      .map((obj) => {
        delete obj.rank
        delete obj.count
        return obj
      })
  )
}

export default searchData
