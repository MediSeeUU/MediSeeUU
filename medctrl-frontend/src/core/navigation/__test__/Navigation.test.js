// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import SideNavigation from '../Navigation'
import AccountPage from '../../../pages/account/AccountPage'
import DataPage from '../../../pages/data/DataPage'
import MockProvider from '../../../mocks/MockProvider'

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

test('render datapage without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <MockProvider>
        <DataPage />
      </MockProvider>
    </BrowserRouter>,
    root
  )
})

test('logout navbarbutton is clickable when logged in', () => {
  render(
    <BrowserRouter>
      <SideNavigation />
    </BrowserRouter>
  )
  const loginbutton = screen.getAllByText('Login')[0]
  expect(fireEvent.click(loginbutton)).toBeTruthy()
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
  expect(fireEvent.click(loginbutton)).toBeTruthy()
})
