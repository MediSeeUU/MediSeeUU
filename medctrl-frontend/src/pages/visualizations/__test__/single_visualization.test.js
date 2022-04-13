import React from 'react'
import ReactDOM from 'react-dom'
import {
  cleanup,
  render,
  fireEvent,
  waitFor,
  screen,
  getByRole,
  getByText,
} from '@testing-library/react'
import VisualizationPage from '../VisualizationPage'
import SingleVisualization from '../single_visualization/SingleVisualization'
import ResizeObserver from '../mocks/observer'

import data from '../data.json'

jest.mock('../mocks/observer')

test('render initial single visualization', () => {
  const root = document.createElement('div')
  ReactDOM.render(<SingleVisualization number={1} data={data} />, root)
})
