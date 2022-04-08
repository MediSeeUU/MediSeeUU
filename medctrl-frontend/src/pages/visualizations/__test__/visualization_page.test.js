import React from 'react'
import ReactDOM from 'react-dom'
import { render, fireEvent, waitFor, screen } from '@testing-library/react'
import VisualizationPage from '../VisualizationPage'
import CategoryOptions from '../single_visualization/forms/shared/CategoryOptions'
import PieForm from '../form_types/pie_form'
import VisualizationForm from '../single_visualization/single_visualization_controller/VisualizationForm'
import SingleVisualization from '../single_visualization/single_visualization_controller/SingleVisualization'

import data from '../data.json'

test('render initial page', () => {
  // need to import ass jest.mock instead of Moch
  require('../__Mocks__/observer.js')
  const root = document.createElement('div')
  ReactDOM.render(<VisualizationPage />, root)
})



test('render initial Category Options', () => {
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
})

test('render initial single visualization', () => {
  require('../__Mocks__/observer.js')
  const root = document.createElement('div')
  ReactDOM.render(<SingleVisualization number={1} data={data} />, root)
})
