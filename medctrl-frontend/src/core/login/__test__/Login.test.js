import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent } from '@testing-library/react'
import SideNavigation from '../../navigation/Navigation'
import { BrowserRouter } from 'react-router-dom'
import handleLogin from '../connectionServer'
/*
import AccountPage from '../../../pages/account/AccountPage'
import MessagesPage from '../../../pages/messages/MessagesPage'
import SearchPage from '../../../pages/search/SearchPage'
import { DataContext } from '../../../shared/contexts/DataContext'
import allData from '../../../testJson/data.json'
import Table from '../../../shared/table/table'
import SettingsPage from '../../../pages/settings/SettingsPage'
import {
  CheckedContext,
  CheckedContextUpdate,
  ColumnSelectionContext,
  ColumnSelectionContextUpdate,
} from '../../../shared/contexts/DataContext'
import DataPage from '../../../pages/data/DataPage'
import { InfoPage } from '../../../pages/detailed-info/DetailedInfoPage'
import proceduredataTest from '../../../pages/detailed-info/detailed-info-data.json'
*/
test("open and close login popup", ()=>{
  
    const defUser = {
        isAdmin: true,
        userName: 'Lourens Bloem',
        accessLevel: 'X',
      }
      render(
        <BrowserRouter>
          <SideNavigation loggedin={false} user={defUser} />
        </BrowserRouter>
      )
      var loginbutton = screen.getAllByText('Login')[0]
      fireEvent.click(loginbutton)
      var cancelbutton = screen.getByText("Cancel")
      fireEvent.click(cancelbutton)

})

function delay(time){
      return new Promise(resolve => setTimeout(resolve, time))
    }


    
global.fetch = jest.fn(() => 
      Promise.resolve({
        json: () => Promise.resolve({ user:{username:'gebruiksnaam', groups:[{name:'groepsnaam0'}]}, access:'X', token:'777' }),
      }) 
    )

beforeEach(() => { fetch.mockClear()})




test("click login and try faulty login credentials should give error message", async ()=>{
     /* jest.mock(handleLogin)
     handleLogin()
     handleLogin.mockResolvedValue
    const asyncmockLOGIN = jest.fn().mockResolvedValue(VALUE HIERRR)
     */
    //overide global fetch function with fake/mock version 
    


      render(
        <BrowserRouter>
          <SideNavigation/>
        </BrowserRouter>
      )
      const loginbutton = screen.getAllByText('Login')[0]
      fireEvent.click(loginbutton)
      const signinbutton = screen.getByText('Sign in')
      console.log(signinbutton.innerHTML)
      fireEvent.click(signinbutton)
      
      const errorContainer = await delay(1000).then(() => screen.getByText('An Error Occurred'))
      //expect(errorContainer).toBeTruthy()
      console.log(errorContainer.innerHTML)

})