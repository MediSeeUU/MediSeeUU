import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import SideNavigation from '../Navigation'
import AccountPage from '../../../pages/account/AccountPage'
import SettingsPage from '../../../pages/settings/SettingsPage'
import DataPage from '../../../pages/data/DataPage'
import Provider from '../../../shared/Provider'

test('sidenavigation component renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <SideNavigation />
    </BrowserRouter>,
    root
  )
})

test('sidenavigation bar should expand or collapse navbar after toggle', () => {
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

test('render settingspage without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <SettingsPage />
    </BrowserRouter>,
    root
  )
})

test('render datapage without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <Provider mock={true}>
        <DataPage />
      </Provider>
    </BrowserRouter>,
    root
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
  const loginbutton = screen.getAllByText('Login')[0]
  expect(fireEvent.click(loginbutton)).toBe(true)
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

  const loginbutton = screen.getAllByTestId('navaccountbutton')[0]
  expect(fireEvent.click(loginbutton)).toBe(true)
})
