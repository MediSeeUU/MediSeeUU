import React from 'react'
import ReactDOM from 'react-dom'
import { render, screen, fireEvent, within } from '@testing-library/react'
import Table from '../table'
import DummyData from '../../../testJson/data.json'
import {
  CheckedContext,
  CheckedContextUpdate,
} from '../../contexts/DataContext'

test('renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <Table data={DummyData} currentPage={1} amountPerPage={10} />,
    root
  )
})

test('expected amount of rows in the table', () => {
  render(
    <Table
      data={DummyData}
      currentPage={1}
      amountPerPage={DummyData.length + 10}
    />
  )
  const table = screen.getByRole('table')
  const rows = within(table).getAllByRole('row')
  expect(rows).toHaveLength(DummyData.length + 1)
})

test('expected amount of headers in the table', () => {
  render(<Table data={DummyData} currentPage={1} amountPerPage={10} />)
  const table = screen.getByRole('table')
  const rows = within(table).getAllByRole('row')
  const headers = within(rows[0]).queryAllByRole('columnheader')
  expect(headers).toHaveLength(Object.keys(DummyData[0]).length)
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
  const view = render(
    <CheckedContext.Provider value={checkedState}>
      <CheckedContextUpdate.Provider value={setCheckedState}>
        <Table
          data={data}
          selectTable={true}
          currentPage={1}
          amountPerPage={10}
        />
      </CheckedContextUpdate.Provider>
    </CheckedContext.Provider>
  )
  const table = screen.getByRole('table')
  const checkboxes = within(table).getAllByRole('checkbox')
  expect(checkboxes).toHaveLength(11)
})

test('row selected, when checkbox clicked', () => {
  let checkedState = Object.assign(
    {},
    ...DummyData.map((entry) => ({ [entry.EUNumber]: false }))
  )
  const setCheckedState = (newState) => {
    checkedState = newState
  }

  const view = render(
    <CheckedContext.Provider value={checkedState}>
      <CheckedContextUpdate.Provider value={setCheckedState}>
        <Table
          data={data}
          selectTable={true}
          setCheckedState={setCheckedState}
          checkedState={checkedState}
          currentPage={2}
          amountPerPage={10}
        />
      </CheckedContextUpdate.Provider>
    </CheckedContext.Provider>
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

  const view = render(
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
  const renderFunction = () =>
    render(
      <Table
        dataToParent={() => {}}
        selectTable={true}
        currentPage={1}
        amountPerPage={10}
      />
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when currentPage not defined', () => {
  const renderFunction = () =>
    render(
      <Table
        Table
        data={DummyData}
        dataToParent={() => {}}
        selectTable={true}
        amountPerPage={10}
      />
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when amountPerPage not defined', () => {
  const renderFunction = () =>
    render(
      <Table
        Table
        data={DummyData}
        dataToParent={() => {}}
        currentPage={5}
        selectTable={true}
      />
    )
  expect(renderFunction).toThrow(Error)
})

test('throw error when current page does not exist', () => {
  const renderFunction = () =>
    render(
      <Table
        Table
        data={DummyData}
        dataToParent={() => {}}
        currentPage={5000}
        amountPerPage={100}
        selectTable={true}
      />
    )
  expect(renderFunction).toThrow(Error)
})

test('data put correctly into table', () => {
  render(
    <Table
      data={DummyData}
      selectTable={true}
      setCheckedState={() => {}}
      checkedState={Array(DummyData.length).fill(false)}
      currentPage={1}
      amountPerPage={10}
    />
  )
  const headers = screen.getAllByRole('columnheader')
  const rowgroup = screen.getAllByRole('rowgroup')[1]
  const rows = within(rowgroup).getAllByRole('row')
  headers.forEach((header, index) => {
    const select = within(header).getByRole('combobox')
    const selectValue = select.value
    rows.forEach((row, index2) => {
      const cells = within(row).getAllByRole('cell')
      const cellValue = cells[index + 1].innerHTML
      const dataElement = DummyData[index2]
      expect(cellValue).toBe(dataElement[selectValue].toString())
    })
  })
})

test('column change changes data in row', () => {
  render(
    <Table
      data={DummyData}
      selectTable={true}
      setCheckedState={() => {}}
      checkedState={Array(DummyData.length).fill(false)}
      currentPage={1}
      amountPerPage={10}
    />
  )
  const headers = screen.queryAllByRole('columnheader')
  const firstSelect = within(headers[0]).getByRole('combobox')
  const startValue = firstSelect.value
  const options = within(firstSelect).getAllByRole('option')
  const newValue = options[1].value
  expect(startValue).not.toBe(newValue)
  fireEvent.change(firstSelect, { target: { value: newValue } })
  const rowgroup = screen.getAllByRole('rowgroup')[1]
  const rows = within(rowgroup).getAllByRole('row')
  rows.forEach((row, index) => {
    const cells = within(row).getAllByRole('cell')
    const cellValue = cells[1].innerHTML
    const dataElement = DummyData[index]
    expect(cellValue).toBe(dataElement[newValue].toString())
  })
})
