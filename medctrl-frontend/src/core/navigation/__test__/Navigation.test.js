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

test('text input in searchbar should return correct search results', () => {
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

test('logout navbarbutton is clickable when logged in', () => {
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
})

test('logout navbarbutton is clickable when logged in2', () => {

  sessionStorage.setItem('username', 'Sjoerd heart minecraft')
  sessionStorage.setItem('access_level', 'X')
  sessionStorage.setItem('token', 'oh zon mooi token')

  render(
    <BrowserRouter>
      <SideNavigation />
    </BrowserRouter>
  )

  sessionStorage.clear()

  var loginbutton = screen.getAllByTestId('navaccountbutton')[0]
  fireEvent.click(loginbutton)
})
