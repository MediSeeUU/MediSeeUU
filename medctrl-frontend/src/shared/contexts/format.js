// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import { defaultColumns } from './ColumnSelectionContext'

// Function that cleans the fetched data from the API based on the given structure data
export default function cleanFetchedData(fetchedData, structData) {
  const cleanedData = []
  for (var i = 0; i < fetchedData.length; ++i) {
    const dataPoint = fetchedData[i]
    // The datapoint should only be included if it is a valid datapoint
    // This is the case when it has a non null eunumber (Short EU Number)
    if (dataPoint.eunumber && structData) {
      cleanedData.push(cleanFetchedDataPoint(dataPoint, structData))
    }
  }
  return cleanedData
}

// Function that cleans a single datapoint
function cleanFetchedDataPoint(fetchedDataPoint, structData) {
  const cleanedDataPoint = {}

  // Format the individual value into the correct format, if the
  // value is null or undefined, a default value is returned
  const format = (value, def, type) => {
    if (
      value === null ||
      value === undefined ||
      value === '' ||
      value === 'unknown' ||
      value === 'NA'
    ) {
      return def
    }

    switch (type) {
      case 'number':
        return parseInt(value)
      case 'bool':
        return value === 0 ? 'No' : 'Yes'
      case 'string':
        return value.toString()
      case 'link':
        return value.toString()
      case 'date': {
        // Y-M-D ->  M/D/Y
        let splitteddate = value.split('-')
        return splitteddate[1] + '/' + splitteddate[2] + '/' + splitteddate[0]
      }
      default:
        return def
    }
  }

  // Each of the variable fields retrieved from the backend are mapped to
  // their respective frontend fields and the data values are formatted accordingly
  for (let category in structData) {
    for (var i = 0; i < structData[category].length; ++i) {
      const backKey = structData[category][i]['data-key']
      const frontKey = structData[category][i]['data-front-key']
      var defValue = 'NA'
      const typeValue = structData[category][i]['data-format']

      cleanedDataPoint[frontKey] = format(
        fetchedDataPoint[backKey],
        defValue,
        typeValue
      )
    }
  }

  // The decision year can be derived from the year of the decision date (M/D/Y)
  let DecisionYear = defValue
  let DecisionDate = cleanedDataPoint['DecisionDate']
  if (DecisionDate === defValue) {
    DecisionYear = defValue
    cleanedDataPoint['DecisionYear'] = DecisionYear
  } else if (DecisionDate) {
    DecisionYear = parseInt(DecisionDate.split('/')[2])
    cleanedDataPoint['DecisionYear'] = DecisionYear
  }

  defaultColumns.forEach((key) => {
    if (cleanedDataPoint[key] === null || cleanedDataPoint[key] === undefined) {
      throw new Error('Invalid data, default column data not given')
    }
  })

  return cleanedDataPoint
}
