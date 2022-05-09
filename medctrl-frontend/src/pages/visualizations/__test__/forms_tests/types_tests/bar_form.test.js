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
import BarForm from '../../../single_visualization/forms/types/BarForm'

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
    stacked: false,
    stackType: false,
    horizontal: false,
  }
})

test('initial render', () => {
  const onChange = jest.fn()
  render(
    <BarForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
})

test('category change', () => {
  const onChange = jest.fn()
  var test = render(
    <BarForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
  const target = screen.getByRole('checkbox', { name: /united kingdom/i })
  fireEvent.click(target)
})

test('horizontal option on', () => {
  const onChange = jest.fn()
  render(
    <BarForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
  const target = screen.getByRole('checkbox', { name: /horizontal/i })
  fireEvent.click(target)
})
