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
let graphSetting
beforeAll(() => {
  uniqueCategories = GetUniqueCategories(data)
  graphSetting = {
    xAxis: 'DecisionYear',
    yAxis: 'Rapporteur',
    categoriesSelected: [],
    stacked: false,
    stackType: false,
    horizontal: false,
    selectAllCategories: false,
    eligibleVariables: []
  }
})

test('initial render', () => {
  const onChange = jest.fn()
  render(<LineForm uniqueCategories={uniqueCategories} onChange={onChange} graphSettings={graphSetting} />)
})

test('category change', () => {
  const onChange = jest.fn()
  render(<LineForm uniqueCategories={uniqueCategories} onChange={onChange} graphSettings={graphSetting} />)
  const target = screen.getByRole('checkbox', { name: /united kingdom/i })
  fireEvent.click(target)
})

test('xaxis change', () => {
  const onChange = jest.fn()
  render(<LineForm uniqueCategories={uniqueCategories} onChange={onChange} graphSettings={graphSetting} />)
  let target = screen.getByRole('combobox', { name: /x-axis/i })
  fireEvent.change(target, { target: { value: 'Rapporteur' } })
})
