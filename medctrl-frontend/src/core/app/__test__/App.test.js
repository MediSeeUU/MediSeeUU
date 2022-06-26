// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import ReactDOM from 'react-dom'
import App from '../App.js'

test('App component renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(<App />, root)
})
