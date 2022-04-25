import {
  cleanup,
  render,
  fireEvent,
  waitFor,
  screen,
  getByRole,
  getByText,
} from '@testing-library/react'
import sortCategoryData from '../../single_visualization/utils/SortCategoryData'
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'

import data from '../../../../testJson/data.json'

test('no data', () => {
  const data = []
  const uniqueCategories = GetUniqueCategories(data)
  const expectedDict = {}
  expect(uniqueCategories).toStrictEqual(expectedDict)
  expect(() => sortCategoryData(uniqueCategories['Rapporteur'])).toThrow()
})

test('some elements', () => {
  const dataSubset = data.slice(0, 20)
  const uniqueCategories = GetUniqueCategories(dataSubset)
  expect(Object.keys(uniqueCategories)).toHaveLength(28)
  const sortedCategory = sortCategoryData(uniqueCategories['Rapporteur'])
  expect(sortedCategory).toHaveLength(8)
})
