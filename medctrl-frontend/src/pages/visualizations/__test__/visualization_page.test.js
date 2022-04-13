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

// rendering a visualization page and adding a visualization
test('add a visualization', () => {
  render(<VisualizationPage/>)
  fireEvent.click(screen.getByRole('button', { name: /add visualization/i }))
  // we start with 1 visualization and add another
  expect(screen.getAllByRole('button', { name: /export as svg/i }).length).toEqual(2)
})

// rendering a visualization page, then removing the initial visualization
test('remove a visualization', () => {
  render(<VisualizationPage />)
  // the removal button is currently the only button with no text
  fireEvent.click(screen.getByRole('button', { name: ''}))
  expect(screen.queryAllByText(/export as svg/i).length).toEqual(0)
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


