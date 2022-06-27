// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import { render, fireEvent, screen } from '@testing-library/react'
import getUniqueCategories from '../../../single_visualization/utils/getUniqueCategories'
import CategoryOptions from '../../../single_visualization/forms/shared/CategoryOptions'
import sortCategoryData from '../../../single_visualization/utils/sortCategoryData'
import data from '../../../../../json/data.json'

const uniqueCategories = getUniqueCategories(data)

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
