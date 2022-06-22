// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
// Filter data based on the given filters
function filterData(data, filters) {
  let updatedData = [...data]
  filters.forEach((item) => {
    switch (item.filterType) {
      case 'string':
        updatedData = textFilter(updatedData, item)
        break
      case 'number':
        updatedData = numFilter(updatedData, item)
        break
      case 'date':
        updatedData = dateFilter(updatedData, item)
        break
      case 'bool':
        updatedData = textFilter(updatedData, item)
        break
      default:
        break
    }
  })
  return updatedData
}

// Function that applies one filter item to the data
function textFilter(data, item) {
  if (!item.selected) {
    return data
  }
  return data.filter((obj) => {
    return item.input.some((x) =>
      obj[item.selected].toString().toLowerCase().includes(x.var.toLowerCase())
    )
  })
}

function numFilter(data, item) {
  if (!item.selected) {
    return data
  }
  return data.filter((obj) => {
    return item.input.every((x) => {
      if (x.filterRange === 'from') {
        return x.var <= obj[item.selected]
      }
      if (x.filterRange === 'till') {
        return x.var >= obj[item.selected]
      } else {
        throw new Error('Filter range invalid')
      }
    })
  })
}

function dateFilter(data, item) {
  if (!item.selected) {
    return data
  }
  return data.filter((obj) => {
    const itemDate = new Date(obj[item.selected])
    return item.input.every((x) => {
      if (x.filterRange === 'from') {
        const xDate = new Date(x.var)
        return xDate <= itemDate
      } else if (x.filterRange === 'till') {
        const xDate = new Date(x.var)
        return xDate >= itemDate
      } else {
        throw new Error('Invalid filter type')
      }
    })
  })
}

export default filterData
