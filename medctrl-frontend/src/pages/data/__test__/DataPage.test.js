// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'
import ReactDOM from 'react-dom'
import { render, fireEvent, screen, within } from '@testing-library/react'
import DataPage from '../DataPage.js'
import DataSelect from '../data_select/DataSelect.js'
import SelectedData from '../selected_data/SelectedData.js'
import { BrowserRouter } from 'react-router-dom'
import MockProvider from '../../../mocks/MockProvider'
import mockObject from '../../../mocks/mockObject'

test('DataPage renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <MockProvider>
        <DataPage />
      </MockProvider>
    </BrowserRouter>,
    root
  )
})

test('DataSelect renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <MockProvider>
        <DataSelect />
      </MockProvider>
    </BrowserRouter>,
    root
  )
})

test('SelectedData renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <MockProvider>
        <SelectedData selectedData={[]} />
      </MockProvider>
    </BrowserRouter>,
    root
  )
})

test('data can be cleared', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <DataPage />
      </MockProvider>
    </BrowserRouter>
  )
  const table = screen.getAllByRole('table')[1]
  const rows = within(table).getAllByRole('row')
  expect(rows.length).toBeGreaterThan(1)
  const clear = screen.getByTestId('clear-all-label')
  fireEvent.click(clear)
  expect(screen.getAllByRole('table')).toHaveLength(1)
})

test('data can be selected', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <DataPage />
      </MockProvider>
    </BrowserRouter>
  )

  // Get main table
  const table = screen.getAllByRole('table')[0]

  // Get the content if the first column of the first row
  const firstRow = screen.getAllByRole('row')[1]

  // select the first entry in the main table
  const checkBox = within(table).getAllByRole('checkbox')
  fireEvent.click(checkBox[0])
  fireEvent.click(checkBox[1])

  // There should now be 2 tables.
  const tables = screen.getAllByRole('table')
  expect(tables).toHaveLength(2)

  // get the final row (AKA the row in the second table)
  const rows = screen.getAllByRole('row')
  const lastRow = rows[rows.length - 1]

  // the first row (selected entry) and last row (displayed entry) should have the same content
  expect(firstRow.textContent).toBe(lastRow.textContent)
})

test('available pages lower than current loaded', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <DataPage />
      </MockProvider>
    </BrowserRouter>
  )

  // Move to a higher page number
  const nextPage = screen.getAllByTestId('next-page-table')[0]

  for (let i = 8; i >= 0; i--) {
    fireEvent.click(nextPage)
  }

  // Change the amount of entries per page to 300, so that the current page number no longer exists
  const resPerPage = screen.getAllByDisplayValue('25')[0]
  fireEvent.change(resPerPage, { target: { value: 300 } })
})

test('amount of pages is 3', () => {
  const mock = { ...mockObject, data: mockObject.data.slice(0, 70) }
  render(
    <BrowserRouter>
      <MockProvider mock={mock}>
        <DataPage />
      </MockProvider>
    </BrowserRouter>
  )

  // There should now be only 3 page options. 3 page options and 1 arrow buttons means the
  // pagination div should now have 4 childnodes.
  const paginationDiv = screen.getAllByTestId('pagination-div')[0]

  expect(paginationDiv.childNodes).toHaveLength(4)
})

test('Can go a page forward and backwards', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <DataPage />
      </MockProvider>
    </BrowserRouter>
  )

  const nextPage = screen.getAllByTestId('next-page-table')[0]

  // Going forward 5 pages
  for (let i = 5; i >= 0; i--) {
    fireEvent.click(nextPage)
  }

  const prevPage = screen.getAllByTestId('prev-page-table')[0]

  const paginationDiv = screen.getAllByTestId('pagination-div')[0]

  // After 5 clicks, the current page should be 7
  expect(paginationDiv.childNodes[4].textContent.trim()).toBe('7')

  fireEvent.click(prevPage)

  // clicking the previous page button once should bring the current page to 6
  expect(paginationDiv.childNodes[4].textContent.trim()).toBe('6')
})

test('search button pressed', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <DataPage />
      </MockProvider>
    </BrowserRouter>
  )
  const input = screen.getByRole('textbox')
  fireEvent.change(input, { target: { value: 'pfizer' } })
  const button = screen.getByText(/Search/i)
  expect(fireEvent.click(button)).toBeTruthy()
})

test('menu apply is pressed', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <DataPage />
      </MockProvider>
    </BrowserRouter>
  )
  const button = screen.getByText(/Filter & Sort/i)
  fireEvent.click(button)
  const apply = screen.getByText(/Apply/i)
  expect(fireEvent.click(apply)).toBeTruthy()
})

test('sort button is pressed', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <DataPage />
      </MockProvider>
    </BrowserRouter>
  )
  const button = screen.getAllByTestId('sort-asc-column')[0]
  expect(fireEvent.click(button)).toBeTruthy()
})
