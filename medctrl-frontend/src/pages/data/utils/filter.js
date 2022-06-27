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

// Text filter
function textFilter(data, item) {
  // If no item is selected, then just return the data
  if (!item.selected) {
    return data
  }
  return data.filter((obj) => {
    return item.input.some((x) => {
      // If custom input is given, then the filter is only partial
      if (x.custom) {
        return  obj[item.selected].toString().toLowerCase().includes(x.var.toLowerCase())
      }
      // Otherwise they must match exactly
      return obj[item.selected].toString().toLowerCase() === x.var.toLowerCase()
    }
    )
  })
}

// Numerical filter
function numFilter(data, item) {
  // If no item is selected, then just return the data
  if (!item.selected) {
    return data
  }
  return data.filter((obj) => {
    // Filter the data based on the given numerical range
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

// Date filter
function dateFilter(data, item) {
  // If no item is selected, then just return the data
  if (!item.selected) {
    return data
  }
  // Filter the data based on the given date range
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
