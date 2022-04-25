import {
  cleanup,
  render,
  fireEvent,
  waitFor,
  screen,
  getByRole,
  getByText,
} from '@testing-library/react'
import GetUniqueCategories from '../../../single_visualization/utils/GetUniqueCategories'
import CategoryOptions from '../../../single_visualization/forms/shared/CategoryOptions'
import sortCategoryData from '../../../single_visualization/utils/SortCategoryData'

import data from '../../../../../testJson/data.json'

let uniqueCategories
beforeAll(() => {
  uniqueCategories = GetUniqueCategories(data)
})

test('initial render', () => {
  const onChange = jest.fn()
  render(
    <CategoryOptions
      key={1}
      className={'category-options'}
      onChange={onChange}
      categories={sortCategoryData(uniqueCategories['Rapporteur'])}
    />
  )
})

test('add and remove a category', () => {
  const onChange = jest.fn()
  render(
    <CategoryOptions
      key={1}
      className={'category-options'}
      onChange={onChange}
      categories={sortCategoryData(uniqueCategories['Rapporteur'])}
    />
  )
  const target = screen.getByRole('checkbox', { name: /united kingdom/i })
  fireEvent.click(target)
  fireEvent.click(target)
})

test('remove category when it was not first selected', () => {
  const onChange = jest.fn()
  render(
    <CategoryOptions
      key={1}
      className={'category-options'}
      onChange={onChange}
      categories={sortCategoryData(uniqueCategories['Rapporteur'])}
    />
  )
  const target = screen.getByRole('checkbox', { name: /united kingdom/i })
  fireEvent.click(target, { target: { checked: false } })
})

test('select and deselect all categories', () => {
  const onChange = jest.fn()
  render(
    <CategoryOptions
      key={1}
      className={'category-options'}
      onChange={onChange}
      categories={sortCategoryData(uniqueCategories['Rapporteur'])}
    />
  )
  const target = screen.getByRole('checkbox', {
    name: /select all categories/i,
  })
  fireEvent.click(target)
  fireEvent.click(target)
})
