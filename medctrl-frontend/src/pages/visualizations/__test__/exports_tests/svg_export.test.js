// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import ReactDOM from 'react-dom'
import { fireEvent, screen } from '@testing-library/react'
import SingleVisualization from '../../single_visualization/SingleVisualization'
import ResizeObserver from '../../mocks/observer'
import data from '../../../../json/data.json'
import getUniqueCategories from '../../single_visualization/utils/getUniqueCategories'

jest.mock('../../mocks/observer')

test('export to svg', () => {
  const unique = getUniqueCategories(data)
  let setting = {
    id: 1,
    chartType: 'bar',
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelectedX: unique['DecisionYear'],
      categoriesSelectedY: unique['Rapporteur'],
    },
    legendOn: true,
    labelsOn: false,
    data: data,
    uniqueCategories: unique,
  }

  let container = document.createElement('div')
  document.body.append(container)

  URL.createObjectURL = jest.fn()
  ReactDOM.render(<SingleVisualization id={1} settings={setting} />, container)
  let target = screen.getByRole('button', { name: /export as svg/i })
  fireEvent.click(target)
})
