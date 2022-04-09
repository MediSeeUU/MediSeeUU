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
import SingleVisualization from '../single_visualization/single_visualization_controller/SingleVisualization'
import ResizeObserver from '../mocks/observer'
import IntersectionObserver from '../mocks/IntersectionObserver'

import data from '../data.json'

beforeAll(() => {
  // IntersectionObserver isn't available in test environment
  const mockIntersectionObserver = jest.fn()
  mockIntersectionObserver.mockReturnValue({
    observe: () => null,
    unobserve: () => null,
    disconnect: () => null,
  })
  window.IntersectionObserver = mockIntersectionObserver
})

jest.mock('../mocks/observer')
jest.mock('../mocks/IntersectionObserver')

// test if the initial page renders as a stand alonte without crashing
/* test('render initial page', () => {
  const root = document.createElement('div')
  ReactDOM.render(<VisualizationPage />, root)
  
}) */

//
test('add a visualization', () => {
  const visualizationsArray = [
    { name: 'visualization1' },
    { name: 'visualization2' },
  ]

  let view = render(<SingleVisualization number={1} data={data} />)

  //fireEvent.click(view.getByText('Add visualization'))

  //expect(view.getAllByText('Remove visualization').length).toEqual(2)
})

/* test('render initial Category Options', () => {
  const root = document.createElement('div')
  ReactDOM.render(<CategoryOptions categories={[]} />, root)
})

test('render initial Pie form', () => {
  const root = document.createElement('div')
  let categories = {}
  categories['Rapporteur'] = []
  ReactDOM.render(<PieForm uniqueCategories={categories} />, root)
})

test('render initial form', () => {
  const root = document.createElement('div')
  let categories = {}
  categories['Rapporteur'] = []
  ReactDOM.render(<VisualizationForm uniqueCategories={categories} />, root)
}) */

test('render initial single visualization', () => {
  screen.debug()
  const root = document.createElement('div')
  ReactDOM.render(<SingleVisualization number={1} data={data} />, root)
})
