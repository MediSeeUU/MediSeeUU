// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import SideNavigation from '../../navigation/Navigation'
import { BrowserRouter } from 'react-router-dom'

test('open and close login popup', () => {
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
  var cancelbutton = screen.getByText('Cancel')
  fireEvent.click(cancelbutton)
})
