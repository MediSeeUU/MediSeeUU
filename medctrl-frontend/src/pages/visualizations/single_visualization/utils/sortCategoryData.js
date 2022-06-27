// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

// sorting function for the categories
export default function sortCategoryData(category) {
  return category.sort(function (a, b) {
    return String(a).localeCompare(b, 'en', {
      numeric: true,
      sensitivity: 'base',
    })
  })
}
