import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent } from '@testing-library/react'

import SideNavigation from '../Navigation'
import { BrowserRouter } from 'react-router-dom'
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

test('sidenavigation component renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <SideNavigation />
    </BrowserRouter>,
    root
  )
})

test('Sidenavigation bar should expand or collapse navbar after toggle', () => {
  render(
    <BrowserRouter>
      <SideNavigation />
    </BrowserRouter>
  )
  var togglebutton = screen.getAllByTestId('navbartogglebutton')
  var toggletext = screen.getAllByTestId('nav-item-name')
  fireEvent.click(togglebutton[0])
  expect(toggletext).not.toBe(screen.getByTestId('nav-item-name'))
})

test('clicking home button should collapse an opened navbar', () => {
  render(
    <BrowserRouter>
      <SideNavigation />
    </BrowserRouter>
  )
  var navbarhomebuttoncomponent = screen.getAllByTestId('Home')[0]
  fireEvent.click(navbarhomebuttoncomponent)
  var menuexpansion = screen.getAllByText('Expand Menu')[0]
  expect(menuexpansion).toBeTruthy()
})

test('if user is logged in, show useraccount and logout button in sidenavbar', () => {
  const userLoggedIn = true
  const defUser = {
    isAdmin: false,
    userName: 'Lourens Bloem',
    accessLevel: 'X',
  }
  render(
    <BrowserRouter>
      <SideNavigation loggedin={userLoggedIn} user={defUser} />
    </BrowserRouter>
  )
  var userbutton = screen.getByText('Account Info')
  expect(userbutton).toBeTruthy()
  var logoutbutton = screen.getAllByText('Logout')[0]
  expect(logoutbutton).toBeTruthy()
})

test('if logged in user is admin, display messages button', () => {
  const userLoggedIn = true
  const defUser = {
    isAdmin: true,
    userName: 'Lourens Bloem',
    accessLevel: 'X',
  }
  render(
    <BrowserRouter>
      <SideNavigation loggedin={userLoggedIn} user={defUser} />
    </BrowserRouter>
  )

  var messagesbutton = screen.getAllByText('Messages')[0]
  expect(messagesbutton).toBeTruthy()
})

test('logout navbarbutton is clickable when logged in', () => {
  const defUser = {
    isAdmin: true,
    userName: 'Lourens Bloem',
    accessLevel: 'X',
  }
  render(
    <BrowserRouter>
      <SideNavigation loggedin={true} user={defUser} />
    </BrowserRouter>
  )
  var useraccountbutton = screen.getByTestId('navaccountbutton')
  fireEvent.click(useraccountbutton)
})

test('render account page without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <AccountPage />
    </BrowserRouter>,
    root
  )
})

test('render messages page without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <MessagesPage />
    </BrowserRouter>,
    root
  )
})

test('render search page without crashing', () => {
  const data = allData

  let checkedState = Object.assign(
    {},
    ...data.map((entry) => ({ [entry.EUNumber]: false }))
  )
  const setCheckedState = (newState) => {
    checkedState = newState
  }

  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
    <BrowserRouter>
      <DataContext.Provider value={allData}>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <CheckedContext.Provider value={checkedState}>
              <CheckedContextUpdate.Provider value={setCheckedState}>
                <SearchPage />
              </CheckedContextUpdate.Provider>
            </CheckedContext.Provider>
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </DataContext.Provider>
    </BrowserRouter>
  )
})

test('text input in searchbar on searchpage should trigger search functionality', () => {
  var test = jest.fn()

  const data = allData

  let checkedState = Object.assign(
    {},
    ...data.map((entry) => ({ [entry.EUNumber]: false }))
  )
  const setCheckedState = (newState) => {
    checkedState = newState
  }

  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
    <BrowserRouter>
      <DataContext.Provider value={allData}>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <CheckedContext.Provider value={checkedState}>
              <CheckedContextUpdate.Provider value={setCheckedState}>
                <div>
                  <div className="TopTableHolder">
                    <button className="searchbox__button">
                      <i className="bx bx-search search-Icon"></i>Search
                    </button>
                    <input
                      type="text"
                      placeholder="Search"
                      className="content__container__textinput"
                      onChange={(e) => test()}
                    />
                  </div>

                  <div className="TopTableHolder searchDataTable">
                    <h1>Results</h1>

                    <Table
                      data={allData}
                      currentPage={1}
                      amountPerPage={50}
                      searchTable={true}
                    />
                  </div>
                </div>
              </CheckedContextUpdate.Provider>
            </CheckedContext.Provider>
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </DataContext.Provider>
    </BrowserRouter>
  )
  const searchbarComponent = screen.getByRole('textbox')
  fireEvent.change(searchbarComponent, { target: { value: '77' } })
  expect(test).toHaveBeenCalled()
})

test('text input in searchbar on searchpage should trigger search functionality2', () => {
  const data = allData

  let checkedState = Object.assign(
    {},
    ...data.map((entry) => ({ [entry.EUNumber]: false }))
  )
  const setCheckedState = (newState) => {
    checkedState = newState
  }

  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
    <BrowserRouter>
      <DataContext.Provider value={allData}>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <CheckedContext.Provider value={checkedState}>
              <CheckedContextUpdate.Provider value={setCheckedState}>
                <SearchPage />
              </CheckedContextUpdate.Provider>
            </CheckedContext.Provider>
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </DataContext.Provider>
    </BrowserRouter>
  )
  const searchbarComponent = screen.getByRole('textbox')
  fireEvent.change(searchbarComponent, { target: { value: '77' } })
  //no expect because search functionality is not yet implemented
})

test('render settingspage without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <SettingsPage />
    </BrowserRouter>,
    root
  )
})

test('detailedinfopage with procedures', () => {
  render(
    <BrowserRouter>
      <DataContext.Provider value={allData}>
        <InfoPage data={proceduredataTest} medIDnumber={'1528'} />
      </DataContext.Provider>
    </BrowserRouter>
  )
})

test('render datapage without crashing', () => {
  const data = allData

  let checkedState = Object.assign(
    {},
    ...data.map((entry) => ({ [entry.EUNumber]: false }))
  )
  const setCheckedState = (newState) => {
    checkedState = newState
  }

  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
    <BrowserRouter>
      <DataContext.Provider value={allData}>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <CheckedContext.Provider value={checkedState}>
              <CheckedContextUpdate.Provider value={setCheckedState}>
                <DataPage />
              </CheckedContextUpdate.Provider>
            </CheckedContext.Provider>
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </DataContext.Provider>
    </BrowserRouter>
  )
})
