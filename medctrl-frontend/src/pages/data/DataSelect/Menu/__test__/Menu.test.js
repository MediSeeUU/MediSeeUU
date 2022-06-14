// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'
import ReactDOM from 'react-dom'
import { render, fireEvent, screen } from '@testing-library/react'
import Menu from '../Menu'
import MockProvider from '../../../../../mocks/MockProvider'

test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(<Menu filters={[]} sorters={[]} />, root)
})

test('opens menu after clicking button', () => {
  render(<Menu filters={[]} sorters={[]} />)
  const button = screen.getByText(/Filter & Sort/i)
  expect(fireEvent.click(button)).toBeTruthy()
  const close = screen.getByText(/Close/i)
  expect(fireEvent.click(close)).toBeTruthy()
})

test('apply button calls update function', () => {
  const update = jest.fn()
  render(<Menu filters={[]} sorters={[]} update={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(update).not.toHaveBeenCalled()
  fireEvent.click(screen.getByText(/Apply/i))
  expect(update).toHaveBeenCalled()
})

test('clear button calls update function', () => {
  const update = jest.fn()
  render(<Menu filters={[]} sorters={[]} update={update} />)
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  expect(update).not.toHaveBeenCalled()
  fireEvent.click(screen.getByText(/Clear/i))
  expect(update).toHaveBeenCalled()
})

test('clear button resets filters and sorters', () => {
  const update = (filters, sorters) => {
    expect(filters).toEqual([
      {
        selected: '',
        input: [{ var: '', filterRange: 'from' }],
        filterType: '',
      },
    ])
    expect(sorters).toEqual([{ selected: '', order: 'asc' }])
  }
  render(<Menu filters={[]} sorters={[]} update={update} />)
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

test('filters and sorters applied correctly in state', () => {
  const update = (filters, sorters) => {
    expect(filters).toStrictEqual([
      {
        filterType: 'text',
        selected: 'ActiveSubstance',
        input: [{ var: 'welcome', filterRange: 'from' }],
      },
    ])
    expect(sorters).toStrictEqual([{ selected: 'ATCCodeL2', order: 'desc' }])
  }
  render(
    <MockProvider>
      <Menu
        filters={[{ selected: '', input: [{ var: '', filterRange: 'from' }] }]}
        sorters={[{ selected: '', order: 'asc' }]}
        update={update}
      />
    </MockProvider>
  )
  fireEvent.click(screen.getByText(/Filter & Sort/i))

  const select1 = screen.getAllByTestId('filter-select')[0]
  fireEvent.change(select1, { target: { value: 'ActiveSubstance' } })
  const text1 = screen.getAllByTestId('filter-input-text')[0]
  fireEvent.change(text1, { target: { value: 'welcome' } })
  fireEvent.focusOut(text1)

  const select2 = screen.getAllByTestId('sort-select-attr')[0]
  fireEvent.change(select2, { target: { value: 'ATCCodeL2' } })
  const order2 = screen.getAllByTestId('sort-select-order')[0]
  fireEvent.change(order2, { target: { value: 'desc' } })

  fireEvent.click(screen.getByText(/Apply/i))
  fireEvent.click(screen.getByText(/Filter & Sort/i))
})
