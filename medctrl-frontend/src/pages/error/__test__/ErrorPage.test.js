import React from 'react'
import ReactDOM from 'react-dom'
import ErrorPage from '../ErrorPage'

test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(<ErrorPage />, root)
})
