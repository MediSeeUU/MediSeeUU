// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import SideNavigation from '../../navigation/Navigation'
import { BrowserRouter } from 'react-router-dom'

test('open and close login popup', async () => {
  render(
    <BrowserRouter>
      <SideNavigation />
    </BrowserRouter>
  )
  const loginbutton = screen.getAllByText('Login')[0]
  expect(fireEvent.click(loginbutton)).toBeTruthy()
  await fetch('/api/account/login')
  const cancelbutton = screen.getByText('Cancel')
  expect(fireEvent.click(cancelbutton)).toBeTruthy()
})
