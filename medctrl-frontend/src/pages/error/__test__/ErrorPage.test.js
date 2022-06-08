// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'
import ReactDOM from 'react-dom'
import ErrorPage from '../ErrorPage'

test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(<ErrorPage />, root)
})
