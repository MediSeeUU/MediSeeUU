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
import GenerateBarSeries from '../single_visualization/data_interfaces/BarInterface'
import GetUniqueCategories from '../single_visualization/utils/GetUniqueCategories'

import data from '../data.json'

test('no selected categories', () => {
	const uniqueCategories = GetUniqueCategories[data]
  const options = {chartSpecificOptions: 
    {xAxis: 'DecisionYear', yAxis: 'Rapporteur'}}
  console.log(GetUniqueCategories(data)[options.chartSpecificOptions.xAxis])
  GenerateBarSeries(
    options, 
    uniqueCategories, 
    data)	
})