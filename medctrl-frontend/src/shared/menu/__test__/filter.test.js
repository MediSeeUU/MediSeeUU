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

test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(<Filter item={{ selected: null, input: [''] }} />, root)
})

test('delete filter function is called', () => {
  const del = jest.fn()
  render(<Filter id={10} item={{ selected: null, input: [''] }} del={del} />)
  fireEvent.click(screen.getByTestId('delete-icon'))
  expect(del).toHaveBeenCalled()
})

test('delete filter returns correct id', () => {
  const del = (id) => {
    expect(id).toBe(10)
  }
  render(<Filter id={10} item={{ selected: null, input: [''] }} del={del} />)
  fireEvent.click(screen.getByTestId('delete-icon'))
})

test('add filter box function is called', () => {
  const box = jest.fn()
  render(<Filter id={10} item={{ selected: null, input: [''] }} box={box} />)
  fireEvent.click(screen.getByTestId('add-label'))
  expect(box).toHaveBeenCalled()
})

test('add filter box returns correct id', () => {
  const box = (id) => {
    expect(id).toBe(7)
  }
  render(<Filter id={7} item={{ selected: null, input: [''] }} box={box} />)
  fireEvent.click(screen.getByTestId('add-label'))
})

test('delete filter box function is called', () => {
  const dbox = jest.fn()
  render(<Filter id={10} item={{ selected: null, input: [''] }} dbox={dbox} />)
  fireEvent.click(screen.getByTestId('remove-icon'))
  expect(dbox).toHaveBeenCalled()
})

test('delete filter box returns correct ids', () => {
  const dbox = (id, bid) => {
    expect(id).toBe(4)
    expect(bid).toBe(2)
  }
  render(<Filter id={4} item={{ selected: null, input: ['hi', 'there', 'this needs to be removed', 'this not'] }} dbox={dbox} />)
  const removes = screen.getAllByTestId('remove-icon')
  fireEvent.click(removes[2])
})

test('change selected function is called', () => {
  const sel = jest.fn()
  render(<Filter id={10} item={{ selected: null, input: [''] }} sel={sel} />)
  const select = screen.getByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'can be anything' } })
  expect(sel).toHaveBeenCalled()
})

test('change selected returns correct id and value', () => {
  const sel = (id, value) => {
    expect(id).toBe(12)
    expect(value).toBe('can be anything')
  }
  render(<Filter id={12} options={<option value='can be anything'>this should not matter</option>} item={{ selected: null, input: [''] }} sel={sel} />)
  const select = screen.getByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'can be anything' } })
})

test('change input function is called', () => {
  const fil = jest.fn()
  render(<Filter id={10} item={{ selected: null, input: [''] }} fil={fil} />)
  const input = screen.getByTestId('filter-input')
  fireEvent.change(input, { target: { value: 'can be anything' } })
  fireEvent.focusOut(input)
  expect(fil).toHaveBeenCalled()
})

test('change input function returns correct ids and value', () => {
  const fil = (id, index, value) => {
    expect(id).toBe(52)
    expect(index).toBe(1)
    expect(value).toBe('can be anything')
  }
  render(<Filter id={52} item={{ selected: null, input: ['hi', 'there', 'again'] }} fil={fil} />)
  const inputs = screen.getAllByTestId('filter-input')
  fireEvent.change(inputs[1], { target: { value: 'can be anything' } })
  fireEvent.focusOut(inputs[1])
})
