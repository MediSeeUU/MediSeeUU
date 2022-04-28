import React from 'react'
import ReactDOM from 'react-dom'

import { InfoPage } from '../DetailedInfoPage'
import allData from '../../../testJson/data.json'
import medDataWithProcedures from '../../../../src/pages/detailed-info/detailed-info-data.json'

test('render detailedinfopage without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <InfoPage data={allData} medIDnumber={'1528'} />,

    root
  )
})

test('render detailedinfopage with procedure data', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <InfoPage data={medDataWithProcedures} medIDnumber={'1528'} />,
    root
  )
})

test('render detailedinfopage with unknown medID', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <InfoPage data={medDataWithProcedures} medIDnumber={'nonExistant'} />,
    root
  )
})
