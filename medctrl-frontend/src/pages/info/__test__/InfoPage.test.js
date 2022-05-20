import React from 'react'
import ReactDOM from 'react-dom'
import InfoPage from '../InfoPage'

test('info page renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(<InfoPage />, root)
})
