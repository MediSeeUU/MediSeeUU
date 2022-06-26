// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import { render, fireEvent, screen } from '@testing-library/react'
import getUniqueCategories from '../../../single_visualization/utils/getUniqueCategories'
import BarForm from '../../../single_visualization/forms/types/BarForm'
import data from '../../../../../json/data.json'

const uniqueCategories = getUniqueCategories(data)
let chartSpecificOptions
beforeEach(() => {
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
  render(
    <BarForm
      uniqueCategories={uniqueCategories}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
})

test('category change', () => {
  const mock = jest.fn()
  render(
    <BarForm
      uniqueCategories={uniqueCategories}
      onChange={mock}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
  const target = screen.getByRole('checkbox', { name: /united kingdom/i })
  fireEvent.click(target)
})

test('horizontal option on (switch axes)', () => {
  chartSpecificOptions.horizontal = true
  render(
    <BarForm
      uniqueCategories={uniqueCategories}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
})

test('stacked option on', () => {
  chartSpecificOptions.stacked = true
  render(
    <BarForm
      uniqueCategories={uniqueCategories}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
})

test('xaxis change', () => {
  const onChange = jest.fn()
  render(
    <BarForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
  let target = screen.getByRole('combobox', { name: /x\-axis/i })
  fireEvent.change(target, { target: { name: 'xAxis', value: 'Rapporteur' } })
})

test('yaxis change', () => {
  const onChange = jest.fn()
  render(
    <BarForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      chartSpecificOptions={chartSpecificOptions}
    />
  )
  let target = screen.getByRole('combobox', { name: /y\-axis/i })
  fireEvent.change(target, { target: { name: 'yAxis', value: 'DecisionYear' } })
})
