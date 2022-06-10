import React from 'react'
import ReactDOM from 'react-dom'
import { fireEvent, screen } from '@testing-library/react'
import SingleVisualization from '../../single_visualization/SingleVisualization'
import ResizeObserver from '../../mocks/observer'

import data from '../../../../json/data.json'
import getUniqueCategories from '../../single_visualization/utils/getUniqueCategories'

jest.mock('../../mocks/observer')

// Does not seem to go beyond the dataURI function,
// may take too long?
test('export to png', () => {
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

  ReactDOM.render(<SingleVisualization id={1} settings={setting} />, container)
  let target = screen.getByRole('button', { name: /export as png/i })
  fireEvent.click(target)
})
