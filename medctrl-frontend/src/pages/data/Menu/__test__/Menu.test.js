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
import Menu from '../Menu'

test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(<Menu filters={[]} sorters={[]} />, root)
})

test('opens menu after clicking button', () => {
  render(<Menu filters={[]} sorters={[]} />)
  expect(screen.queryByLabelText(/Menu/i)).not.toBeInTheDocument()
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(screen.getByLabelText(/Menu/i)).toBeInTheDocument()
})

test('apply button calls update function', () => {
  const update1 = jest.fn()
  const update2 = jest.fn()
  render(
    <Menu
      filters={[]}
      sorters={[]}
      updateFilters={update1}
      updateSorters={update2}
    />
  )
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(update1).not.toHaveBeenCalled()
  expect(update2).not.toHaveBeenCalled()
  fireEvent.click(screen.getByText(/Apply/i))
  expect(update1).toHaveBeenCalled()
  expect(update2).toHaveBeenCalled()
})

test('clear button calls update function', () => {
  const update1 = jest.fn()
  const update2 = jest.fn()
  render(
    <Menu
      filters={[]}
      sorters={[]}
      updateFilters={update1}
      updateSorters={update2}
    />
  )
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(update1).not.toHaveBeenCalled()
  expect(update2).not.toHaveBeenCalled()
  fireEvent.click(screen.getByText(/Clear/i))
  expect(update1).toHaveBeenCalled()
  expect(update2).toHaveBeenCalled()
})

test('clear button resets filters and sorters', () => {
  const update1 = (filters) =>
    expect(filters).toEqual([{ selected: '', input: [''] }])
  const update2 = (sorters) =>
    expect(sorters).toEqual([{ selected: '', order: 'asc' }])
  render(
    <Menu
      filters={[]}
      sorters={[]}
      updateFilters={update1}
      updateSorters={update2}
    />
  )
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  fireEvent.click(screen.getByText(/Clear/i))
})

test('close button closes menu', () => {
  render(<Menu filters={[]} sorters={[]} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  fireEvent.click(screen.getByText(/Close/i))
  expect(screen.queryByLabelText(/Menu/i)).not.toBeInTheDocument()
})

test('add filter adds filter item', () => {
  render(<Menu filters={[{ selected: '', input: [''] }]} sorters={[]} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(screen.queryAllByTestId('filter-select')).toHaveLength(1)
  fireEvent.click(screen.getByText(/Add Filter/i))
  expect(screen.queryAllByTestId('filter-select')).toHaveLength(2)
})

// test for checking if clicking the "Add sorting option" label adds an sorting-item (A)
test('add sorting option adds sorting item', () => {
  render(<Menu filters={[]} sorters={[{ selected: '', order: 'asc' }]} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(screen.queryAllByTestId('sort-select-attr')).toHaveLength(1)
  fireEvent.click(screen.getByText(/Add Sorting option +/i))
  expect(screen.queryAllByTestId('sort-select-attr')).toHaveLength(2)
})

// test for checking if clicking the X button to remove sorting option removes an sorting-item when this item is not the last sorting box (A)
test('remove sorting option removes sorting item', () => {
  render(<Menu filters={[]} sorters={[{ selected: '', order: 'asc' }]} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  //add 2nd sorting option box
  fireEvent.click(screen.getByText(/Add Sorting option +/i))
  expect(screen.queryAllByTestId('sort-select-attr')).toHaveLength(2)
  //remove the second option sorting box only
  fireEvent.click(screen.getAllByTestId('delete-sorting-box')[1])
  expect(screen.queryAllByTestId('sort-select-attr')).toHaveLength(1)
})

test('max 4 filters', () => {
  render(<Menu filters={[]} sorters={[{ selected: '', order: 'asc' }]} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const addSort = screen.getByText(/Add Sorting option +/i)
  fireEvent.click(addSort)
  fireEvent.click(addSort)
  fireEvent.click(addSort)
  expect(addSort).not.toBeInTheDocument()
})

test('add filterbox', () => {
  render(<Menu filters={[{ selected: '', input: [''] }]} sorters={[]} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(screen.getAllByRole('textbox')).toHaveLength(1)
  fireEvent.click(screen.getByText('+ Add'))
  expect(screen.getAllByRole('textbox')).toHaveLength(2)
})

test('remove filterbox', () => {
  render(<Menu filters={[{ selected: '', input: [''] }]} sorters={[]} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  fireEvent.click(screen.getByText('+ Add'))
  expect(screen.getAllByRole('textbox')).toHaveLength(2)
  fireEvent.click(screen.getAllByTestId('remove-icon')[0])
  expect(screen.getAllByRole('textbox')).toHaveLength(1)
})

test('always have one filterbox', () => {
  render(<Menu filters={[{ selected: '', input: [''] }]} sorters={[]} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(screen.getAllByRole('textbox')).toHaveLength(1)
  fireEvent.click(screen.getByTestId('remove-icon'))
  expect(screen.getAllByRole('textbox')).toHaveLength(1)
})

test('remove filter', () => {
  render(<Menu filters={[{ selected: '', input: [''] }]} sorters={[]} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  fireEvent.click(screen.getByText(/Add Filter/i))
  expect(screen.queryAllByTestId('filter-select')).toHaveLength(2)
  fireEvent.click(screen.getAllByTestId('delete-icon')[0])
  expect(screen.queryAllByTestId('filter-select')).toHaveLength(1)
})

const list = [
  <option value="dummy1" key={1}>
    hi
  </option>,
  <option value="dummy2" key={2}>
    there
  </option>,
]

test('saved filters in state', () => {
  render(
    <Menu filters={[{ selected: '', input: [''] }]} sorters={[]} list={list} />
  )
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  fireEvent.click(screen.getByText(/Add Filter/i))

  const select1 = screen.getAllByTestId('filter-select')[0]
  fireEvent.change(select1, { target: { value: 'dummy2' } })
  const text1 = screen.getAllByTestId('filter-input')[0]
  fireEvent.change(text1, { target: { value: 'welcome' } })
  fireEvent.focusOut(text1)

  const select2 = screen.getAllByTestId('filter-select')[1]
  fireEvent.change(select2, { target: { value: 'dummy1' } })
  const text2 = screen.getAllByTestId('filter-input')[1]
  fireEvent.change(text2, { target: { value: 'again' } })
  fireEvent.focusOut(text2)

  fireEvent.click(screen.getByText(/Close/i))
  fireEvent.click(screen.getByText(/Filter & Sort/i))

  expect(screen.getAllByTestId('filter-select')[0].value).toBe('dummy2')
  expect(screen.getAllByTestId('filter-select')[1].value).toBe('dummy1')
  expect(screen.getAllByTestId('filter-input')[0].value).toBe('welcome')
  expect(screen.getAllByTestId('filter-input')[1].value).toBe('again')
})

test('saved sorters in state', () => {
  render(
    <Menu filters={[]} sorters={[{ selected: '', order: 'asc' }]} list={list} />
  )
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  fireEvent.click(screen.getByText(/Add Sorting option +/i))

  const select1 = screen.getAllByTestId('sort-select-attr')[0]
  fireEvent.change(select1, { target: { value: 'dummy1' } })
  const order1 = screen.getAllByTestId('sort-select-order')[0]
  fireEvent.change(order1, { target: { value: 'desc' } })

  const select2 = screen.getAllByTestId('sort-select-attr')[1]
  fireEvent.change(select2, { target: { value: 'dummy2' } })
  const order2 = screen.getAllByTestId('sort-select-order')[1]
  fireEvent.change(order2, { target: { value: 'asc' } })

  fireEvent.click(screen.getByText(/Close/i))
  fireEvent.click(screen.getByText(/Filter & Sort/i))

  expect(screen.getAllByTestId('sort-select-attr')[0].value).toBe('dummy1')
  expect(screen.getAllByTestId('sort-select-attr')[1].value).toBe('dummy2')
  expect(screen.getAllByTestId('sort-select-order')[0].value).toBe('desc')
  expect(screen.getAllByTestId('sort-select-order')[1].value).toBe('asc')
})
