import React from 'react'
import ReactDOM from 'react-dom'
import {
  render,
  fireEvent,
  screen,
} from '@testing-library/react'
import Search from '../Search'

test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(<Search />, root)
})

test('initial query is set in textbox', () => {
  render(<Search initial="pfizer" />)
  const input = screen.getByRole('textbox')
  expect(input.value).toBe('pfizer')
})

test('update is called on enter press', () => {
  const update = jest.fn()
  render(<Search update={update} />)
  const input = screen.getByRole('textbox')
  fireEvent.focusIn(input)
  fireEvent.change(input, { target: { value: 'pfizer' } })
  fireEvent.keyDown(input, { key: 'Enter', code: 13, charCode: 13 })
  expect(update).toHaveBeenCalled()
})

test('update is not called on other key presses', () => {
  const update = jest.fn()
  render(<Search update={update} />)
  const input = screen.getByRole('textbox')
  fireEvent.focusIn(input)
  fireEvent.change(input, { target: { value: 'pfizer' } })
  fireEvent.keyDown(input, { key: 'Space', code: 'Space' })
  expect(update).not.toHaveBeenCalled()
})

test('update is called on button click', () => {
  const update = jest.fn()
  render(<Search update={update} />)
  const input = screen.getByRole('textbox')
  fireEvent.focusIn(input)
  fireEvent.change(input, { target: { value: 'merck' } })
  const button = screen.getByRole('button')
  fireEvent.click(button)
  expect(update).toHaveBeenCalled()
})

test('update returns right query on enter press', () => {
  const update = (query) => {
    expect(query).toStrictEqual(new String('pfizer'))
  }
  render(<Search update={update} />)
  const input = screen.getByRole('textbox')
  fireEvent.focusIn(input)
  fireEvent.change(input, { target: { value: 'pfizer' } })
  fireEvent.keyDown(input, { key: 'Enter', code: 13, charCode: 13 })
})

test('update returns right query on button click', () => {
  const update = (query) => {
    expect(query).toStrictEqual(new String('merck'))
  }
  render(<Search update={update} />)
  const input = screen.getByRole('textbox')
  fireEvent.focusIn(input)
  fireEvent.change(input, { target: { value: 'merck' } })
  const button = screen.getByRole('button')
  fireEvent.click(button)
})

test('clear button clears query', () => {
  const update = (query) => {
    expect(query).toBe('')
  }
  render(<Search update={update} />)
  const input = screen.getByRole('textbox')
  fireEvent.focusIn(input)
  fireEvent.change(input, { target: { value: 'pfizer' } })
  const clear = screen.getByTestId('search-close-icon')
  fireEvent.click(clear)
})
