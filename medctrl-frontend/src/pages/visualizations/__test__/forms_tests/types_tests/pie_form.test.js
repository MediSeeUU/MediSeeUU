import { render, fireEvent, screen } from '@testing-library/react'
import getUniqueCategories from '../../../single_visualization/utils/getUniqueCategories'
import PieForm from '../../../single_visualization/forms/types/PieForm'

import data from '../../../../../json/data.json'

const uniqueCategories = getUniqueCategories(data)
let chartSpecificOptions
beforeEach(() => {
  chartSpecificOptions = {
    xAxis: 'Rapporteur',
    categoriesSelectedX: uniqueCategories['Rapporteur'],
  }
})

test('initial render', () => {
  render(
    <PieForm
      uniqueCategories={uniqueCategories}
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
    target: { value: 'Rapporteur', name: 'xAxis' },
  })
})
