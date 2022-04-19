import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent, within } from '@testing-library/react'
import Table from '../table'
import DummyData from '../../../testJson/data.json'
import {
  CheckedContext,
  CheckedContextUpdate,
  ColumnSelectionContext,
  ColumnSelectionContextUpdate,
} from '../../contexts/DataContext'

test('renders without crashing', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const root = document.createElement('div')
  ReactDOM.render(
    <ColumnSelectionContext.Provider value={columnSelection}>
      <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
        <Table data={DummyData} currentPage={1} amountPerPage={10} />
      </ColumnSelectionContextUpdate.Provider>
    </ColumnSelectionContext.Provider>,
    root
  )
})

test('expected amount of rows in the table', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
    <ColumnSelectionContext.Provider value={columnSelection}>
      <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
        <Table
          data={DummyData}
          currentPage={1}
          amountPerPage={DummyData.length + 10}
        />
      </ColumnSelectionContextUpdate.Provider>
    </ColumnSelectionContext.Provider>
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
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
    <ColumnSelectionContext.Provider value={columnSelection}>
      <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
        <Table data={DummyData} currentPage={1} amountPerPage={10} />
      </ColumnSelectionContextUpdate.Provider>
    </ColumnSelectionContext.Provider>
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
    ...data.map((entry) => ({ [entry.EUNumber]: false }))
  )
  const setCheckedState = (newState) => {
    checkedState = newState
  }

  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
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
  )
  const table = screen.getByRole('table')
  const checkboxes = within(table).getAllByRole('checkbox')
  expect(checkboxes).toHaveLength(11)
})

test('row selected, when checkbox clicked', () => {
  const data = DummyData
  let checkedState = Object.assign(
    {},
    ...DummyData.map((entry) => ({ [entry.EUNumber]: false }))
  )
  const setCheckedState = (newState) => {
    checkedState = newState
  }

  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
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
  )
  const table = screen.getByRole('table')
  const input = within(table).getAllByRole('checkbox')[1]
  fireEvent.click(input)
  expect(checkedState[DummyData[10].EUNumber]).toBe(true)
})

test('all rows selected when select all pressed', () => {
  const data = DummyData
  let checkedState = Object.assign(
    {},
    ...data.map((entry) => ({ [entry.EUNumber]: false }))
  )
  const setCheckedState = (newState) => {
    checkedState = newState
  }

  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
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
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const renderFunction = () =>
    render(
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table currentPage={1} amountPerPage={10} />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when currentPage not defined', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const renderFunction = () =>
    render(
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table data={DummyData} amountPerPage={10} />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when amountPerPage not defined', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const renderFunction = () =>
    render(
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table data={DummyData} currentPage={1} />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when current page does not exist', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const renderFunction = () =>
    render(
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table data={DummyData} currentPage={500000} amountPerPage={10} />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    )
  expect(renderFunction).toThrow(Error)
})

test('data put correctly into table', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  render(
    <ColumnSelectionContext.Provider value={columnSelection}>
      <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
        <Table data={DummyData} currentPage={1} amountPerPage={10} />
      </ColumnSelectionContextUpdate.Provider>
    </ColumnSelectionContext.Provider>
  )
  const headers = screen.getAllByRole('columnheader')
  const rowgroup = screen.getAllByRole('rowgroup')[1]
  const rows = within(rowgroup).getAllByRole('row')
  headers.forEach((header, index) => {
    const select = within(header).getByRole('combobox')
    const selectValue = select.value
    rows.forEach((row, index2) => {
      const cells = within(row).getAllByRole('cell')
      const cellValue = cells[index].innerHTML
      const dataElement = DummyData[index2]
      expect(cellValue).toBe(dataElement[selectValue].toString())
    })
  })
})

test('column change changes data in row', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const { rerender } = render(
    <ColumnSelectionContext.Provider value={columnSelection}>
      <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
        <Table data={DummyData} currentPage={1} amountPerPage={10} />
      </ColumnSelectionContextUpdate.Provider>
    </ColumnSelectionContext.Provider>
  )
  const headers = screen.queryAllByRole('columnheader')
  const firstSelect = within(headers[0]).getByRole('combobox')
  const startValue = firstSelect.value
  const options = within(firstSelect).getAllByRole('option')
  const newValue = options[1].value
  expect(startValue).not.toBe(newValue)
  fireEvent.change(firstSelect, { target: { value: newValue } })
  rerender(
    <ColumnSelectionContext.Provider value={columnSelection}>
      <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
        <Table data={DummyData} currentPage={1} amountPerPage={10} />
      </ColumnSelectionContextUpdate.Provider>
    </ColumnSelectionContext.Provider>
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
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const { rerender } = render(
    <ColumnSelectionContext.Provider value={columnSelection}>
      <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
        <Table data={DummyData} currentPage={1} amountPerPage={10} />
      </ColumnSelectionContextUpdate.Provider>
    </ColumnSelectionContext.Provider>
  )
  const initHeaderLength = screen.queryAllByRole('columnheader').length
  fireEvent.click(screen.getAllByRole('button')[0])
  rerender(
    <ColumnSelectionContext.Provider value={columnSelection}>
      <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
        <Table data={DummyData} currentPage={1} amountPerPage={10} />
      </ColumnSelectionContextUpdate.Provider>
    </ColumnSelectionContext.Provider>
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
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const { rerender } = render(
    <ColumnSelectionContext.Provider value={columnSelection}>
      <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
        <Table data={DummyData} currentPage={1} amountPerPage={10} />
      </ColumnSelectionContextUpdate.Provider>
    </ColumnSelectionContext.Provider>
  )

  const initHeaderLength = screen.queryAllByRole('columnheader').length
  fireEvent.click(screen.getAllByRole('button')[1])
  rerender(
    <ColumnSelectionContext.Provider value={columnSelection}>
      <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
        <Table data={DummyData} currentPage={1} amountPerPage={10} />
      </ColumnSelectionContextUpdate.Provider>
    </ColumnSelectionContext.Provider>
  )
  const newHeaderLength = screen.queryAllByRole('columnheader').length

  expect(newHeaderLength).toBe(initHeaderLength - 1)
})

test('Amount of columns does not drop below 4', () => {
  var columnSelection = [
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
    'ApplicationNo',
    'ApplicationNo',
  ]

  const setColumnSelection = (newColumns) => {
    columnSelection = newColumns
  }

  const { rerender } = render(
    <ColumnSelectionContext.Provider value={columnSelection}>
      <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
        <Table data={DummyData} currentPage={1} amountPerPage={10} />
      </ColumnSelectionContextUpdate.Provider>
    </ColumnSelectionContext.Provider>
  )

  let headerLength = screen.queryAllByRole('columnheader').length
  while (headerLength > 5) {
    fireEvent.click(screen.getAllByRole('button')[1])
    rerender(
      <ColumnSelectionContext.Provider value={columnSelection}>
        <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
          <Table data={DummyData} currentPage={1} amountPerPage={10} />
        </ColumnSelectionContextUpdate.Provider>
      </ColumnSelectionContext.Provider>
    )
    headerLength = screen.queryAllByRole('columnheader').length
  }

  fireEvent.click(screen.getAllByRole('button')[1])
  headerLength = screen.queryAllByRole('columnheader').length

  expect(headerLength).toBe(5)
})
