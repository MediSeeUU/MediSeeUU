import { React } from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent, within } from '@testing-library/react'
import Table from '../table'
import DummyData from '../../../testJson/data.json'
import structData from '../../../shared/contexts/structServer.json'
import {
  DataContext,
  SelectedContext,
  CheckedContext,
  CheckedContextUpdate,
  ColumnSelectionContext,
  ColumnSelectionContextUpdate,
  StructureContext,
} from '../../contexts/DataContext'
import { BrowserRouter } from 'react-router-dom'
import { dataToDisplayFormat } from '../../table/table'
import updateData from '../../../pages/data/Utils/update'

test('renders without crashing', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter>
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table data={DummyData} currentPage={1} amountPerPage={10} />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    </BrowserRouter>,
    root
  )
})

test('expected amount of rows in the table', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
    <BrowserRouter>
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table
            data={DummyData}
            currentPage={1}
            amountPerPage={DummyData.length + 10}
          />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    </BrowserRouter>
  )
  const table = screen.getByRole('table')
  const rows = within(table).getAllByRole('row')
  expect(rows).toHaveLength(DummyData.length + 1)
})

test('expected amount of headers in the table', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
    <BrowserRouter>
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table data={DummyData} currentPage={1} amountPerPage={10} />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    </BrowserRouter>
  )
  const table = screen.getByRole('table')
  const rows = within(table).getAllByRole('row')
  const headers = within(rows[0]).queryAllByRole('columnheader')
  expect(headers).toHaveLength(columnSelection.length)
})

test('checkboxes displayed', () => {
  const data = DummyData

  let checkedState = Object.assign(
    {},
    ...data.map((entry) => ({ [entry.EUNoShort]: false }))
  )
  const setCheckedState = (newState) => {
    checkedState = newState
  }

  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
    <BrowserRouter>
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <CheckedContext.Provider value={checkedState}>
            <CheckedContextUpdate.Provider value={setCheckedState}>
              <Table
                data={data}
                selectTable={true}
                setCheckedState={setCheckedState}
                checkedState={checkedState}
                currentPage={2}
                amountPerPage={10}
                testCheckedState={checkedState}
                testCheckedStateUpdate={setCheckedState}
              />
            </CheckedContextUpdate.Provider>
          </CheckedContext.Provider>
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    </BrowserRouter>
  )
  const table = screen.getByRole('table')
  const checkboxes = within(table).getAllByRole('checkbox')
  expect(checkboxes).toHaveLength(11)
})

test('row selected, when checkbox clicked', () => {
  const data = DummyData
  let checkedState = Object.assign(
    {},
    ...DummyData.map((entry) => ({ [entry.EUNoShort]: false }))
  )
  const setCheckedState = (newState) => {
    checkedState = newState
  }

  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
    <BrowserRouter>
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <CheckedContext.Provider value={checkedState}>
            <CheckedContextUpdate.Provider value={setCheckedState}>
              <Table
                data={data}
                selectTable={true}
                setCheckedState={setCheckedState}
                checkedState={checkedState}
                currentPage={2}
                amountPerPage={10}
                testCheckedState={checkedState}
                testCheckedStateUpdate={setCheckedState}
              />
            </CheckedContextUpdate.Provider>
          </CheckedContext.Provider>
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    </BrowserRouter>
  )
  const table = screen.getByRole('table')
  const input = within(table).getAllByRole('checkbox')[1]
  fireEvent.click(input)
  expect(checkedState[DummyData[10].EUNoShort]).toBe(true)
})

test('all rows selected when select all pressed', () => {
  const data = DummyData
  let checkedState = Object.assign(
    {},
    ...data.map((entry) => ({ [entry.EUNoShort]: false }))
  )
  const setCheckedState = (newState) => {
    checkedState = newState
  }

  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
    <BrowserRouter>
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <CheckedContext.Provider value={checkedState}>
            <CheckedContextUpdate.Provider value={setCheckedState}>
              <Table
                data={data}
                selectTable={true}
                setCheckedState={setCheckedState}
                checkedState={checkedState}
                currentPage={2}
                amountPerPage={10}
                testCheckedState={checkedState}
                testCheckedStateUpdate={setCheckedState}
              />
            </CheckedContextUpdate.Provider>
          </CheckedContext.Provider>
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    </BrowserRouter>
  )
  const table = screen.getByRole('table')
  const input = within(table).getAllByRole('checkbox')[0]
  fireEvent.click(input)
  let checkedCount = () => {
    let count = 0
    for (const prop in checkedState) {
      if (checkedState[prop]) {
        count++
      }
    }
    return count
  }
  expect(checkedCount()).toBe(data.length)
})

test('throw error when data not defined', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const renderFunction = () =>
    render(
      <BrowserRouter>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <Table currentPage={1} amountPerPage={10} />
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </BrowserRouter>
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when currentPage not defined', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const renderFunction = () =>
    render(
      <BrowserRouter>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <Table data={DummyData} amountPerPage={10} />
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </BrowserRouter>
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when amountPerPage not defined', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const renderFunction = () =>
    render(
      <BrowserRouter>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <Table data={DummyData} currentPage={1} />
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </BrowserRouter>
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when current page does not exist', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const renderFunction = () =>
    render(
      <BrowserRouter>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <Table data={DummyData} currentPage={500000} amountPerPage={10} />
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </BrowserRouter>
    )
  expect(renderFunction).toThrow(Error)
})

test('data put and displayed correctly into table', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
    <BrowserRouter>
      <StructureContext.Provider value={structData}>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <Table data={DummyData} currentPage={1} amountPerPage={10} />
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </StructureContext.Provider>
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
  var data = DummyData
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }
  let checkedState = Object.assign(
    {},
    ...data.map((entry) => ({ [entry.EUNumber]: true }))
  )

  const selectedData = data.filter((item, index) => {
    return checkedState[item.EUNumber]
  })

  const search = '' // Current search
  const filters = [{ selected: '', input: [''] }] // Current filters

  var sorters = [{ selected: '', order: 'asc' }]
  const setSorters = (newsorter) => {
    sorters = newsorter
  }

  const updatedData = updateData(
    selectedData,
    search,
    filters,
    sorters,
    columnSelection
  )

  render(
    <BrowserRouter>
      <StructureContext.Provider value={structData}>
        <DataContext.Provider value={data}>
          <SelectedContext.Provider value={selectedData}>
            <ColumnSelectionContext.Provider value={columnSelection}>
              <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
                <Table
                  data={updatedData}
                  currentPage={1}
                  amountPerPage={10}
                  setSorters={setSorters}
                />
              </ColumnSelectionContextUpdate.Provider>
            </ColumnSelectionContext.Provider>
          </SelectedContext.Provider>
        </DataContext.Provider>
      </StructureContext.Provider>
    </BrowserRouter>
  )

  const firstcolumndescsortbutton = screen.getAllByText('^')[0]
  fireEvent.click(firstcolumndescsortbutton)
  //table should now be sorted descending on first column attribute value
  const rowgroup = screen.getAllByRole('rowgroup')[1]
  const rows = within(rowgroup).getAllByRole('row')
  var prevrowvalue = rows[0].cells[0].textContent

  rows.forEach((row) => {
    const cellValue = row.cells[0].textContent

    expect(parseInt(cellValue)).toBeGreaterThanOrEqual(parseInt(prevrowvalue))
    prevrowvalue = cellValue
  })
})

test('column change changes data in row', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const { rerender } = render(
    <BrowserRouter>
      <StructureContext.Provider value={structData}>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <Table data={DummyData} currentPage={1} amountPerPage={10} />
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </StructureContext.Provider>
    </BrowserRouter>
  )
  const headers = screen.queryAllByRole('columnheader')
  const firstSelect = within(headers[0]).getByRole('combobox')
  const startValue = firstSelect.value
  const options = within(firstSelect).getAllByRole('option')
  const newValue = options[1].value
  expect(startValue).not.toBe(newValue)
  fireEvent.change(firstSelect, { target: { value: newValue } })
  rerender(
    <BrowserRouter>
      <StructureContext.Provider value={structData}>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <Table data={DummyData} currentPage={1} amountPerPage={10} />
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </StructureContext.Provider>
    </BrowserRouter>
  )

  const newheaders = screen.queryAllByRole('columnheader')
  const newfirstSelect = within(newheaders[0]).getByRole('combobox')
  const newstartValue = newfirstSelect.value
  expect(newstartValue).toBe(newValue)
})

test('Add column button adds a column', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const { rerender } = render(
    <BrowserRouter>
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table data={DummyData} currentPage={1} amountPerPage={10} />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    </BrowserRouter>
  )
  const initHeaderLength = screen.queryAllByRole('columnheader').length
  fireEvent.click(screen.getByTestId('add-column'))
  rerender(
    <BrowserRouter>
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table data={DummyData} currentPage={1} amountPerPage={10} />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    </BrowserRouter>
  )
  const newHeaderLength = screen.queryAllByRole('columnheader').length

  expect(newHeaderLength).toBe(initHeaderLength + 1)
})

test('Remove column button removes a column', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const { rerender } = render(
    <BrowserRouter>
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table data={DummyData} currentPage={1} amountPerPage={10} />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    </BrowserRouter>
  )

  const initHeaderLength = screen.queryAllByRole('columnheader').length
  fireEvent.click(screen.getByTestId('remove-column'))
  rerender(
    <BrowserRouter>
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table data={DummyData} currentPage={1} amountPerPage={10} />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    </BrowserRouter>
  )
  const newHeaderLength = screen.queryAllByRole('columnheader').length

  expect(newHeaderLength).toBe(initHeaderLength - 1)
})

test('Amount of columns does not drop below 5', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const { rerender } = render(
    <BrowserRouter>
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table data={DummyData} currentPage={1} amountPerPage={10} />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    </BrowserRouter>
  )

  let headerLength = screen.queryAllByRole('columnheader').length
  while (headerLength > 5) {
    fireEvent.click(screen.getByTestId('remove-column'))
    rerender(
      <BrowserRouter>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <Table data={DummyData} currentPage={1} amountPerPage={10} />
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </BrowserRouter>
    )
    headerLength = screen.queryAllByRole('columnheader').length
  }

  fireEvent.click(screen.getByTestId('remove-column'))
  headerLength = screen.queryAllByRole('columnheader').length

  expect(headerLength).toBe(5)
})

test('Add column button adds unique variable columns', () => {
  var columnSelection = []
  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const { rerender } = render(
    <BrowserRouter>
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table data={DummyData} currentPage={1} amountPerPage={10} />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    </BrowserRouter>
  )

  for (var i = 0; i < 40; i++) {
    fireEvent.click(screen.getByTestId('add-column'))

    rerender(
      <BrowserRouter>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <Table data={DummyData} currentPage={1} amountPerPage={10} />
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </BrowserRouter>
    )
  }

  const headerLength = screen.queryAllByRole('columnheader').length
  const numberOfUniqueHeaders = Object.keys(DummyData[0]).length
  expect(headerLength).toBe(numberOfUniqueHeaders)
})
