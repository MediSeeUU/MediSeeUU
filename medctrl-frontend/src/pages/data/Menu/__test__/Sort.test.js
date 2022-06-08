// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
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
import Sort from '../Sort'
import structData from '../../../../shared/contexts/structServer.json'
import { StructureContext } from '../../../../shared/contexts/DataContext'

test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(<Sort item={{ selected: 'BrandName', order: 'asc' }} />, root)
})

test('delete sort function is called', () => {
  const del = jest.fn()
  render(
    <Sort id={5} item={{ selected: 'BrandName', order: 'asc' }} del={del} />
  )
  fireEvent.click(screen.getByTestId('delete-sorting-box'))
  expect(del).toHaveBeenCalled()
})

test('delete sort returns correct id', () => {
  const del = (id) => {
    expect(id).toBe(5)
  }
  render(
    <Sort id={5} item={{ selected: 'BrandName', order: 'asc' }} del={del} />
  )
  fireEvent.click(screen.getByTestId('delete-sorting-box'))
})

test('change selected variable function is called', () => {
  const sel = jest.fn()
  render(
    <Sort id={5} item={{ selected: 'BrandName', order: 'asc' }} sel={sel} />
  )
  const select = screen.getByTestId('sort-select-attr')
  fireEvent.change(select, { target: { value: 'can be anything' } })
  expect(sel).toHaveBeenCalled()
})

test('change selected variable returns correct id and value', () => {
  const sel = (id, value) => {
    expect(id).toBe(18)
    expect(value).toBe('BrandName')
  }
  render(
    <StructureContext.Provider value={structData}>
      <Sort
        id={18}
        options={<option value="BrandName">this should not matter</option>}
        item={{ selected: 'BrandName', order: 'asc' }}
        sel={sel}
      />
    </StructureContext.Provider>
  )
  const select = screen.getByTestId('sort-select-attr')
  fireEvent.change(select, { target: { value: 'BrandName' } })
})

test('change selected order function is called', () => {
  const order = jest.fn()
  render(
    <Sort
      id={13}
      item={{ selected: 'BrandName', order: 'asc' }}
      order={order}
    />
  )
  const select = screen.getByTestId('sort-select-order')
  fireEvent.change(select, { target: { value: 'can be anything' } })
  expect(order).toHaveBeenCalled()
})

test('change selected order returns correct id and value', () => {
  const order = (id, value) => {
    expect(id).toBe(27)
    expect(value).toBe('desc')
  }
  render(
    <Sort
      id={27}
      options={<option value="can be anything">this should not matter</option>}
      item={{ selected: 'BrandName', order: 'asc' }}
      order={order}
    />
  )
  const select = screen.getByTestId('sort-select-order')
  fireEvent.change(select, { target: { value: 'desc' } })
})
