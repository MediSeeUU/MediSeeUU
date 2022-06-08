// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
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
import PieForm from '../../../single_visualization/forms/types/PieForm'

import data from '../../../../../testJson/data.json'

let uniqueCategories
let chartSpecificOptions
beforeAll(() => {
  uniqueCategories = GetUniqueCategories(data)
  chartSpecificOptions = {
    xAxis: 'Rapporteur',
    categoriesSelectedX: uniqueCategories['Rapporteur'],
  }
})

test('initial render', () => {
  const onChange = jest.fn()
  render(
    <PieForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
})

test('category change', () => {
  const onChange = jest.fn()
  render(
    <PieForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
  const target = screen.getByRole('checkbox', { name: /united kingdom/i })
  fireEvent.click(target)
})

test('xaxis change', () => {
  const onChange = jest.fn()
  render(
    <PieForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
  let target = screen.getByRole('combobox', { name: /variable/i })
  fireEvent.change(target, {
    target: { value: 'Rapporteur', name: 'chosenVariable' },
  })
})
