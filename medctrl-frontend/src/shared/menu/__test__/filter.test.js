import React from 'react'
import ReactDOM from 'react-dom'
import {
  render,
  fireEvent,
  waitFor,
  screen,
  cleanup,
  within,
} from '@testing-library/react'
import Filter from '../filter'

// Checks if the component renders correctly
test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(<Filter item={{ selected: null, input: [''] }} />, root)
})
