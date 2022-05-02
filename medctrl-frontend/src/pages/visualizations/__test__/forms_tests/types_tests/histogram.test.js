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
import HistogramForm from '../../../single_visualization/forms/types/HistogramForm'

import data from '../../../../../testJson/data.json'

let uniqueCategories
beforeAll(() => {
  uniqueCategories = GetUniqueCategories(data)
})

test('initial render', () => {
  const onChange = jest.fn()
  render(
    <HistogramForm uniqueCategories={uniqueCategories} onChange={onChange} />
  )
})

test('category change', () => {
  const onChange = jest.fn()
  render(
    <HistogramForm uniqueCategories={uniqueCategories} onChange={onChange} />
  )
  const target = screen.getByRole('checkbox', { name: /united kingdom/i })
  fireEvent.click(target)
})

test('xaxis change', () => {
  const onChange = jest.fn()
  render(
    <HistogramForm uniqueCategories={uniqueCategories} onChange={onChange} />
  )
  let target = screen.getByRole('combobox', { name: /variable/i })
  fireEvent.change(target, {
    target: { value: 'Rapporteur', name: 'chosenVariable' },
  })
})
