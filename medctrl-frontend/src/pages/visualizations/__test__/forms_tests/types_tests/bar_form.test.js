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
beforeAll(() => {
	uniqueCategories = GetUniqueCategories(data)
})

test('initial render', () => {
	const onChange = jest.fn()
	render(<BarForm uniqueCategories={uniqueCategories} onChange={onChange} />)
})

test('category change', () => {
	const onChange = jest.fn()
	render(<BarForm uniqueCategories={uniqueCategories} onChange={onChange} />)
	const target = screen.getByRole('checkbox', { name: /united kingdom/i })
	fireEvent.click(target)
})

test('horizontal option on', () => {
	const onChange = jest.fn()
	let barForm = render(<BarForm uniqueCategories={uniqueCategories} onChange={onChange} />)
	const target = screen.getByRole('checkbox', { name: /horizontal/i })
	fireEvent.click(target)
})