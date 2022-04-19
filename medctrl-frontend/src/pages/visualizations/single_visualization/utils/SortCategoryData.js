// sorting function for the categories
export default function sortCategoryData(category) {
  return category.sort(function (a, b) {
    return String(a).localeCompare(b, 'en', {
      numeric: true,
      sensitivity: 'base',
    })
  })
}
