import React from 'react'
import { screen, fireEvent } from '@testing-library/react'
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
