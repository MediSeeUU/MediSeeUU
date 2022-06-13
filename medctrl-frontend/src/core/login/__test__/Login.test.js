import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import SideNavigation from '../../navigation/Navigation'
import { BrowserRouter } from 'react-router-dom'

test('open and close login popup', () => {
  render(
    <BrowserRouter>
      <SideNavigation />
    </BrowserRouter>
  )
  const loginbutton = screen.getByText('Login')[0]
  expect(fireEvent.click(loginbutton)).toBeTruthy()
  const cancelbutton = screen.getByText('Cancel')
  expect(fireEvent.click(cancelbutton)).toBeTruthy()
})
