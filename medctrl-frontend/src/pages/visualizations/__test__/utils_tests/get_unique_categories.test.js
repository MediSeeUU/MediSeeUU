// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import sortCategoryData from '../../single_visualization/utils/sortCategoryData'
import getUniqueCategories from '../../single_visualization/utils/getUniqueCategories'

import data from '../../../../json/data.json'

test('no data', () => {
  const data = []
  const uniqueCategories = getUniqueCategories(data)
  const expectedDict = {}
  expect(uniqueCategories).toStrictEqual(expectedDict)
  expect(() => sortCategoryData(uniqueCategories['Rapporteur'])).toThrow()
})

test('some elements', () => {
  const dataSubset = data.slice(0, 20)
  const uniqueCategories = getUniqueCategories(dataSubset)
  expect(Object.keys(uniqueCategories)).toHaveLength(28)
  const sortedCategory = sortCategoryData(uniqueCategories['Rapporteur'])
  expect(sortedCategory).toHaveLength(8)
})
