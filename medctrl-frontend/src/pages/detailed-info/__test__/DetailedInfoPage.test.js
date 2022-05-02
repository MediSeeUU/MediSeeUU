import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen } from '@testing-library/react'
import { InfoPage } from '../DetailedInfoPage'
import allData from '../../../testJson/data.json'
import medDataWithProcedures from '../../../../src/pages/detailed-info/detailed-info-data.json'

test('render detailedinfopage and display correct data', () => {
  render(<InfoPage data={allData} medIDnumber={'1528'} />)
  var brandnameinfo = screen.getAllByText('Comirnaty')
  expect(brandnameinfo).toBeTruthy()
})

test('render detailedinfopage with temp procedure data', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <InfoPage data={medDataWithProcedures} medIDnumber={'1528'} />,
    root
  )
})

test('render detailedinfopage with unknown medID without crash', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <InfoPage data={medDataWithProcedures} medIDnumber={'000'} />,
    root
  )
})
