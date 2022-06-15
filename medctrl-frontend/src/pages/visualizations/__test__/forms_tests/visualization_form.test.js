// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import { render, fireEvent, screen } from '@testing-library/react'
import getUniqueCategories from '../../single_visualization/utils/getUniqueCategories'
import VisualizationForm from '../../single_visualization/forms/VisualizationForm'

import data from '../../../../json/data.json'

const uniqueCategories = getUniqueCategories(data)
let setting
beforeEach(() => {
  setting = {
    id: 1,
    chartType: 'bar',
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelectedX: uniqueCategories['DecisionYear'],
      categoriesSelectedY: uniqueCategories['Rapporteur'],
    },
    legendOn: true,
    labelsOn: false,
    data: data,
    uniqueCategories: uniqueCategories,
  }
})

test('initial bar chart render', () => {
  render(
    <VisualizationForm uniqueCategories={uniqueCategories} settings={setting} />
  )
})

test('trigger default renderChartOptions', () => {
  const onChange = jest.fn()
  setting.chartType = 'pi'
  expect(() =>
    render(
      <VisualizationForm
        uniqueCategories={uniqueCategories}
        onChange={onChange}
        settings={setting}
      />
    )
  ).toThrow()
})

test('do a chart specific change', () => {
  const onChange = jest.fn()
  render(
    <VisualizationForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      settings={setting}
    />
  )
  let target = screen.getByRole('combobox', { name: /x\-axis/i })

  fireEvent.change(target, {
    target: {
      value: 'Rapporteur',
      name: 'xAxis',
    },
  })
})
