import { React } from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent, within } from '@testing-library/react'
import Table from '../Table'
import serverData from '../../../../../json/allServerData.json'
import structData from '../../../../../json/structServer.json'
import { BrowserRouter } from 'react-router-dom'
import { dataToDisplayFormat } from '../format'
import MockProvider from '../../../../../mocks/mockProvider'
import cleanFetchedData from '../../../../../shared/Contexts/format'

const DummyData = cleanFetchedData(serverData, structData)

test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <MockProvider>
        <Table data={DummyData} currentPage={1} amountPerPage={10} sorters={[{ selected: '', order: 'asc' }]} />
      </MockProvider>
    </BrowserRouter>,
    root
  )
})

test('expected amount of rows in the table', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <Table
          data={DummyData}
          currentPage={1}
          amountPerPage={DummyData.length + 10}
          sorters={[{ selected: '', order: 'asc' }]}
        />
      </MockProvider>
    </BrowserRouter>
  )
  const table = screen.getByRole('table')
  const rows = within(table).getAllByRole('row')
  expect(rows).toHaveLength(DummyData.length + 1)
})

test('expected amount of headers in the table', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <Table data={DummyData} currentPage={1} amountPerPage={10} sorters={[{ selected: '', order: 'asc' }]} />
      </MockProvider>
    </BrowserRouter>
  )
  const table = screen.getByRole('table')
  const rows = within(table).getAllByRole('row')
  const headers = within(rows[0]).queryAllByRole('columnheader')
  expect(headers).toHaveLength(5)
})

test('checkboxes displayed', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <Table
          data={DummyData}
          select={true}
          currentPage={2}
          amountPerPage={10}
          sorters={[{ selected: '', order: 'asc' }]}
        />
      </MockProvider>
    </BrowserRouter>
  )
  const table = screen.getByRole('table')
  const checkboxes = within(table).getAllByRole('checkbox')
  expect(checkboxes).toHaveLength(11)
})

test('row selected, when checkbox clicked', () => {
  const { rerender } = render(
    <BrowserRouter>
      <MockProvider>
        <Table
          data={DummyData}
          select={true}
          currentPage={2}
          amountPerPage={10}
          sorters={[{ selected: '', order: 'asc' }]}
        />
      </MockProvider>
    </BrowserRouter>
  )
  const table = screen.getByRole('table')
  const input = within(table).getAllByRole('checkbox')[1]
  fireEvent.click(input)
  rerender(
    <BrowserRouter>
      <MockProvider>
        <Table
          data={DummyData}
          select={true}
          currentPage={2}
          amountPerPage={10}
          sorters={[{ selected: '', order: 'asc' }]}
        />
      </MockProvider>
    </BrowserRouter>
  )
  expect(input).toBeChecked()
})

test('all rows selected when select all pressed', () => {
  const { rerender } = render(
    <BrowserRouter>
      <MockProvider>
        <Table
          data={DummyData}
          select={true}
          currentPage={2}
          amountPerPage={DummyData.length + 1}
          sorters={[{ selected: '', order: 'asc' }]}
        />
      </MockProvider>
    </BrowserRouter>
  )
  const table = screen.getByRole('table')
  const inputs = within(table).getAllByRole('checkbox')
  fireEvent.click(inputs[0])
  rerender(
    <BrowserRouter>
      <MockProvider>
        <Table
          data={DummyData}
          select={true}
          currentPage={2}
          amountPerPage={DummyData.length + 1}
          sorters={[{ selected: '', order: 'asc' }]}
        />
      </MockProvider>
    </BrowserRouter>
  )
  for (let input of inputs) {
    expect(input).toBeChecked()
  }
})

test('data put and displayed correctly into table', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <Table data={DummyData} currentPage={1} amountPerPage={10} sorters={[{ selected: '', order: 'asc' }]} />
      </MockProvider>
    </BrowserRouter>
  )
  const headers = screen.getAllByRole('columnheader')
  const rowgroup = screen.getAllByRole('rowgroup')[1]
  const rows = within(rowgroup).getAllByRole('row')
  headers.forEach((header, index) => {
    const select = within(header).getByRole('combobox')
    const propt = select.value
    rows.forEach((row, index2) => {
      const cells = within(row).getAllByRole('cell')
      const cellValue = cells[index].textContent
      const entry = DummyData[index2]
      const DisplayedData = dataToDisplayFormat({ entry, propt })
      expect(cellValue).toBe(DisplayedData.toString())
    })
  })
})

test('sorting on leftmost columnheader sorts data', () => {
  const setSorters = (sorters) => {
    expect(sorters).toHaveLength(1) // CHECK OF SORT KLOPT MET WAT GESORTEERD WORDT
  }
  render(
    <BrowserRouter>
      <MockProvider>
        <Table
          data={DummyData}
          currentPage={1}
          amountPerPage={10}
          setSorters={setSorters}
          sorters={[{ selected: '', order: 'asc' }]}
        />
      </MockProvider>
    </BrowserRouter>
  )
  const sortButton = screen.getAllByTestId("sort-asc-column")[0]
  fireEvent.click(sortButton)
})

test('column change changes data in row', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <Table data={DummyData} currentPage={1} amountPerPage={10} sorters={[{ selected: '', order: 'asc' }]} />
      </MockProvider>
    </BrowserRouter>
  )
  const headers = screen.queryAllByRole('columnheader')
  const firstSelect = within(headers[0]).getByRole('combobox')
  const startValue = firstSelect.value
  const options = within(firstSelect).getAllByRole('option')
  const newValue = options[1].value
  expect(startValue).not.toBe(newValue)
  fireEvent.change(firstSelect, { target: { value: newValue } })
  const newheaders = screen.queryAllByRole('columnheader')
  const newfirstSelect = within(newheaders[0]).getByRole('combobox')
  const newstartValue = newfirstSelect.value
  expect(newstartValue).toBe(newValue)
})

test('add and remove columns', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <Table data={DummyData} currentPage={1} amountPerPage={10} sorters={[{ selected: '', order: 'asc' }]} />
      </MockProvider>
    </BrowserRouter>
  )
  const initHeaderLength = screen.queryAllByRole('columnheader').length
  fireEvent.click(screen.getByTestId('add-column'))
  expect(screen.queryAllByRole('columnheader')).toHaveLength(initHeaderLength + 1)
  fireEvent.click(screen.getByTestId('remove-column'))
  expect(screen.queryAllByRole('columnheader')).toHaveLength(initHeaderLength)
})

test('remove button appearing', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <Table data={DummyData} currentPage={1} amountPerPage={10} sorters={[{ selected: '', order: 'asc' }]} />
      </MockProvider>
    </BrowserRouter>
  )
  expect(screen.queryByTestId('remove-column')).not.toBeInTheDocument()
  fireEvent.click(screen.getByTestId('add-column'))
  expect(screen.getByTestId('remove-column')).toBeInTheDocument()
})

test('add column button adds unique variable columns', () => {
  render(
    <BrowserRouter>
      <MockProvider>
        <Table data={DummyData} currentPage={1} amountPerPage={10} sorters={[{ selected: '', order: 'asc' }]} />
      </MockProvider>
    </BrowserRouter>
  )
  const addButton = screen.getByTestId('add-column')
  const numberOfUniqueHeaders = Object.keys(DummyData[0]).length
  for (let i = 0; i < numberOfUniqueHeaders; i++) {
    fireEvent.click(addButton)
  }
  expect(screen.queryByTestId('add-column')).not.toBeInTheDocument()
  const headerLength = screen.queryAllByRole('columnheader').length
  expect(headerLength).toBe(numberOfUniqueHeaders)
})
