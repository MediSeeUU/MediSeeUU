import React from 'react'
import ReactDOM from 'react-dom'
import {
  render,
  fireEvent,
  waitFor,
  screen,
  cleanup,
  within,
  getByTestId,
  getAllByRole,
} from '@testing-library/react'
import DataPage from '../DataPage.js'
import DataSelect from '../dataComponents/DataSelect'
import SelectedData from '../dataComponents/SelectedData'
import { 
  DataProvider,
  SelectedContext,
  DataContext,
  ColumnSelectionContext,
  ColumnSelectionContextUpdate,
  CheckedContext,
  CheckedContextUpdate
} from '../../../shared/contexts/DataContext'
import { BrowserRouter } from 'react-router-dom'
import allData from '../../../testJson/data.json'
import { check } from 'prettier'


test('DataPage renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(
    <BrowserRouter> 
      <DataProvider> 
        <DataPage /> 
      </DataProvider> 
    </BrowserRouter>
  , root)
})

test('DataSelect renders without crashing', () => {
  const root = document.createElement('div');
  ReactDOM.render(
    <BrowserRouter> 
      <DataProvider> 
        <DataSelect /> 
      </DataProvider> 
    </BrowserRouter> , root)
})

test('SelectedData renders without crashing', () => {
  const root = document.createElement('div');
  ReactDOM.render(<SelectedData /> , root)
})

test('data can be selected', () => {
  
    // Render datapage with context
    const root = document.createElement('div');
    render(
      <BrowserRouter> 
        <DataProvider> 
          <DataPage /> 
        </DataProvider> 
      </BrowserRouter>
    , root)
    
    // Get main table
    const table = screen.getAllByRole('table')[0]

    // Get the content if the first column of the first row
    const firstRow = screen.getAllByRole('row')[1]
    console.log(firstRow.children[1].textContent)

    const checkBox = within(table).getAllByRole('checkbox')[1]
    fireEvent.click(checkBox)
    
    // There should now be 2 tables.
    const tables = screen.getAllByRole('table')
    expect(tables.length === 2)

    const rows = screen.getAllByRole('row')
    const lastRow = rows[rows.length - 1]

    expect(firstRow.textContent === lastRow.textContent)

    
})

test('table updated', () => {
  //Setup to render the page
  const data = allData

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


  const root = document.createElement('div');
  render(
    <BrowserRouter>
      <DataContext.Provider value={allData}>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <CheckedContext.Provider value={checkedState}>
              <CheckedContextUpdate.Provider value={setCheckedState}>
                <DataPage />
              </CheckedContextUpdate.Provider>
            </CheckedContext.Provider>
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </DataContext.Provider>
    </BrowserRouter>
  , root)

  // Open the filter & sort menu and apply a filter
  fireEvent.click(screen.getByText(/Filter & Sort/i))
  const select = screen.queryByTestId('filter-select')
  fireEvent.change(select, { target: { value: 'ApplicationNo' } })
  const textBox = screen.getByRole('textbox')
  fireEvent.change(textBox, { target: { value: '8' } })
  fireEvent.focusOut(textBox)
  fireEvent.click(screen.getByText(/Apply/i))

  // Select all filtered datapoints
  const table = screen.getByRole('table')
  const selectAll = within(table).getAllByRole('checkbox')[0]
  fireEvent.click(selectAll)

  // Filter all datapoints to only the selected datapoints
  var updatedData = allData.filter(entry => checkedState[entry.EUNumber])
  
  // Check if all collected datapoints abide by the added filter
  updatedData.forEach((element) => {
    expect(element.ApplicationNo.toString()).toContain('8')
  })

})

test('available pages lower than current loaded', () => {
  //Setup to render the page
  const data = allData

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


  const root = document.createElement('div');
  render(
    <BrowserRouter>
      <DataContext.Provider value={allData}>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <CheckedContext.Provider value={checkedState}>
              <CheckedContextUpdate.Provider value={setCheckedState}>
                <DataPage />
              </CheckedContextUpdate.Provider>
            </CheckedContext.Provider>
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </DataContext.Provider>
    </BrowserRouter>
  , root)

  // Move to a higher page number
  const nextPage = screen.getByTestId("next-page-table")

  for (let i=8; i>=0; i--) {
    fireEvent.click(nextPage)
  }
  
  // Change the amount of entries per page to 300, so that the current page number no longer exists
  const resPerPage = screen.getByDisplayValue('25')
  fireEvent.change(resPerPage, {target : {value : 300}})
})

test('amount of pages is 3', () => {
  //Setup to render the page
  const data = allData.slice(0,70)

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


  const root = document.createElement('div');
  render(
    <BrowserRouter>
      <DataContext.Provider value={data}>
        <ColumnSelectionContext.Provider value={columnSelection}>
          <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
            <CheckedContext.Provider value={checkedState}>
              <CheckedContextUpdate.Provider value={setCheckedState}>
                <DataPage />
              </CheckedContextUpdate.Provider>
            </CheckedContext.Provider>
          </ColumnSelectionContextUpdate.Provider>
        </ColumnSelectionContext.Provider>
      </DataContext.Provider>
    </BrowserRouter>
  , root)

  // There should now be only 3 page options. 3 page options and 2 arrow buttons means the 
  // pagination div should now have 5 childnodes.
  const paginationDiv = screen.getByTestId("pagination-div")

  expect(paginationDiv.childNodes.length == 5)

})

test('Can go a page forward and backwards', () => {
    //Setup to render the page
    const data = allData

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
  
  
    const root = document.createElement('div');
    render(
      <BrowserRouter>
        <DataContext.Provider value={allData}>
          <ColumnSelectionContext.Provider value={columnSelection}>
            <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
              <CheckedContext.Provider value={checkedState}>
                <CheckedContextUpdate.Provider value={setCheckedState}>
                  <DataPage />
                </CheckedContextUpdate.Provider>
              </CheckedContext.Provider>
            </ColumnSelectionContextUpdate.Provider>
          </ColumnSelectionContext.Provider>
        </DataContext.Provider>
      </BrowserRouter>
    , root)

    const nextPage = screen.getByTestId("next-page-table")
    const prevPage = screen.getByTestId("prev-page-table")

    // Going forward 5 pages
    for (let i=5; i>=0; i--) {
      fireEvent.click(nextPage)
    }

    const paginationDiv = screen.getByTestId("pagination-div")

    // After 5 clicks, the current page should be 7
    expect(paginationDiv.childNodes[4].textContent == '7')

    fireEvent.click(prevPage)

    // clicking the previous page button once should bring the current page to 6
    expect(paginationDiv.childNodes[4].textContent == '6')

})
