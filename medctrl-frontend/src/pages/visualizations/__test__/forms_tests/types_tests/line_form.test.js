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
import LineForm from '../../../single_visualization/forms/types/LineForm'

import data from '../../../../../testJson/data.json'

let uniqueCategories
let chartSpecificOptions
beforeAll(() => {
  uniqueCategories = GetUniqueCategories(data)
  chartSpecificOptions = {
    xAxis: 'DecisionYear',
    yAxis: 'Rapporteur',
    categoriesSelectedX: uniqueCategories['DecisionYear'],
    categoriesSelectedY: uniqueCategories['Rapporteur'],
  }
})

test('initial render', () => {
  const onChange = jest.fn()
  render(
    <LineForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
})

test('category change', () => {
  const onChange = jest.fn()
  render(
    <LineForm
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
    <LineForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
  let target = screen.getByRole('combobox', { name: /x-axis/i })
  fireEvent.change(target, { target: { value: 'Rapporteur' } })
})
