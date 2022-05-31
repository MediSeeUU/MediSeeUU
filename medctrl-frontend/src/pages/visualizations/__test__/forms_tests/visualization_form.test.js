import {
  render,
  fireEvent,
  screen,
} from '@testing-library/react'
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'
import VisualizationForm from '../../single_visualization/forms/VisualizationForm'

import data from '../../../../testJson/data.json'

const uniqueCategories = GetUniqueCategories(data)
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
    <VisualizationForm
      uniqueCategories={uniqueCategories}
      settings={setting}
    />
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
  let target = screen.getByRole('combobox', { name: /x-axis/i })

  fireEvent.change(target, {
    target: {
      value: 'Rapporteur',
      name: 'xAxis',
    },
  })
})
