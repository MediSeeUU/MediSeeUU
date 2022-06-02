import { render, fireEvent, screen } from '@testing-library/react'
import GetUniqueCategories from '../../../single_visualization/utils/GetUniqueCategories'
import CategoryOptions from '../../../single_visualization/forms/shared/CategoryOptions'
import sortCategoryData from '../../../single_visualization/utils/SortCategoryData'

import data from '../../../../../testJson/data.json'

const uniqueCategories = GetUniqueCategories(data)

test('initial render', () => {
  render(
    <CategoryOptions
      categories={sortCategoryData(uniqueCategories['Rapporteur'])}
      categoriesSelected={uniqueCategories['Rapporteur']}
    />
  )
})

test('remove a category', () => {
  const onChange = jest.fn()
  render(
    <CategoryOptions
      onChange={onChange}
      categories={sortCategoryData(uniqueCategories['Rapporteur'])}
      categoriesSelected={uniqueCategories['Rapporteur']}
    />
  )
  const target = screen.getByRole('checkbox', { name: /united kingdom/i })
  fireEvent.click(target)
})

test('add a category', () => {
  const onChange = jest.fn()
  render(
    <CategoryOptions
      onChange={onChange}
      categories={sortCategoryData(uniqueCategories['Rapporteur'])}
      categoriesSelected={[]}
    />
  )
  const target = screen.getByRole('checkbox', { name: /united kingdom/i })
  fireEvent.click(target)
})

test('select and deselect all categories', () => {
  const onChange = jest.fn()
  render(
    <CategoryOptions
      onChange={onChange}
      categories={sortCategoryData(uniqueCategories['Rapporteur'])}
      categoriesSelected={uniqueCategories['Rapporteur']}
    />
  )
  const target = screen.getByRole('checkbox', {
    name: /select all categories/i,
  })
  fireEvent.click(target)
  fireEvent.click(target)
})
