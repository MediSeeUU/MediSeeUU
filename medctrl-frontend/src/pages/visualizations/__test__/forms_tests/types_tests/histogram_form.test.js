// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import { render, fireEvent, screen } from '@testing-library/react'
import getUniqueCategories from '../../../single_visualization/utils/getUniqueCategories'
import HistogramForm from '../../../single_visualization/forms/types/HistogramForm'

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
    <HistogramForm
      uniqueCategories={uniqueCategories}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
})

test('category change', () => {
  const onChange = jest.fn()
  render(
    <HistogramForm
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
    <HistogramForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
  let target = screen.getByRole('combobox', { name: /variable/i })
  fireEvent.change(target, {
    target: { value: 'DecisionYear', name: 'xAxis' },
  })
})
