import {
  cleanup,
  render,
  fireEvent,
  waitFor,
  screen,
  getByRole,
  getByText,
} from '@testing-library/react'
import GetUniqueCategories from '../../single_visualization/utils/GetUniqueCategories'
import VisualizationForm from '../../single_visualization/forms/VisualizationForm'

import data from '../../../../testJson/data.json'

let uniqueCategories
let setting
beforeAll(() => {
  uniqueCategories = GetUniqueCategories(data)
  setting = {
    id: 1,
    chartType: 'bar',
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelectedX: uniqueCategories['DecisionYear'],
      categoriesSelectedY: uniqueCategories['Rapporteur'],
    },
    legenOn: true,
    labelsOn: false,
    data: data,
    series: [],
    uniqueCategories: uniqueCategories,
    changeName: '',
  }
})

test('initial render', () => {
  const onChange = jest.fn()
  render(
    <VisualizationForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      settings={setting}
    />
  )
})

test('change to line chart type', () => {
  const onChange = jest.fn()
  render(
    <VisualizationForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      settings={setting}
    />
  )
  let target = screen.getByRole('combobox', { name: /visualization type/i })

  fireEvent.change(target, {
    target: {
      value: 'line',
      name: 'chartType',
    },
  })
})

test('change to pie chart type', () => {
  const onChange = jest.fn()
  render(
    <VisualizationForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      settings={setting}
    />
  )
  let target = screen.getByRole('combobox', { name: /visualization type/i })

  fireEvent.change(target, {
    target: {
      value: 'pie',
      name: 'chartType',
    },
  })
})

test('change to bar chart', () => {
  const onChange = jest.fn()
  render(
    <VisualizationForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      settings={setting}
    />
  )
  let target = screen.getByRole('combobox', { name: /visualization type/i })

  fireEvent.change(target, {
    target: {
      value: 'bar',
      name: 'chartType',
    },
  })
})

test('trigger defaults of resetChartSpecifics and renderChartOptions', () => {
  const onChange = jest.fn()
  render(
    <VisualizationForm
      uniqueCategories={uniqueCategories}
      onChange={onChange}
      settings={setting}
    />
  )
  let target = screen.getByRole('combobox', { name: /visualization type/i })

  expect(() =>
    fireEvent.change(target, {
      target: {
        value: 'pi',
        name: 'chartType',
      },
    })
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
