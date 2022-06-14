// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
//backend received data can be reformatted when displayed in the table
//depeding on the property/variable, different formatting may be applicable
export function dataToDisplayFormat({ entry, propt }) {
  switch (propt) {
    case 'DecisionDate':
      return slashDateToStringDate(entry[propt])
    default:
      return entry[propt]
  }
}

export function slashDateToStringDate(date) {
  const defValue = 'NA'
  if (date === defValue) {
    return date
  }
  var splitteddate = date.split('/')
  const day = splitteddate[1].replace(/^0+/, '')
  const month = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
  ][parseInt(splitteddate[0].replace(/^0+/, '')) - 1]
  const year = splitteddate[2]
  const fullDate = day + ' ' + month + ' ' + year
  return fullDate
}
