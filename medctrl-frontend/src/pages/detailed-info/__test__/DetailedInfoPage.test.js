import React from 'react'
import ReactDOM from 'react-dom'
import {
  render,
  fireEvent,
  screen,
} from '@testing-library/react'
import { InfoPage , DetailedInfoPage} from '../DetailedInfoPage'
import allData from '../../../testJson/data.json'
import medDataWithProcedures from '../../../../src/pages/detailed-info/detailed-info-data.json'
import { BrowserRouter , Route} from 'react-router-dom'
import {DataContext, DataProvider} from '../../../shared/contexts/DataContext'

test('render detailedinfopage and display correct data', () => {
  
  render(
    <InfoPage data={allData} medIDnumber={'1528'} />
  )
  var brandnameinfo = screen.getAllByText("Comirnaty")
  expect(brandnameinfo).toBeTruthy()
})

test('render detailedinfopage with correct procedure data', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <InfoPage data={medDataWithProcedures} medIDnumber={'1528'} />,
    root
  )
  //correct info present
  var proceduredate = screen.getAllByText("2020-12-21")[0]
  expect(proceduredate).toBeTruthy()
  //correct number of procedures displayed
  var procedureBoxesAmount = screen.getAllByText("Decision Date").length
  expect(procedureBoxesAmount).toEqual(4)
})

test('render detailedinfopage with unknown medID', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <InfoPage data={medDataWithProcedures} medIDnumber={'nonExistant'} />,
    root
  )
  var errortext = screen.getAllByText("Unknown Medicine ID Number")[0]
  expect(errortext).toBeTruthy()
})

test('render detailinfopage from routing', ()=>{
  const root = document.createElement('div')
  ReactDOM.render(
    <DataProvider>
      <DataContext.Consumer>
         <BrowserRouter>
           <Route path='details/1528'>
            <DetailedInfoPage />
          </Route>
        </BrowserRouter>
      </DataContext.Consumer>
    </DataProvider>, root

    
  
  )

})
