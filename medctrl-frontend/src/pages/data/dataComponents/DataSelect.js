import React, { useState, useRef } from 'react'
import Menu from '../Menu/Menu'
import Search from '../../../shared/Search/Search'
import TableView from './TableView'
import {
  useData,
  useColumnSelection,
} from '../../../shared/contexts/DataContext'
import updateData from '../Utils/update'

function DataSelect({ initialSearch }) {
  const [resultsPerPage, setResultsPerPage] = useState(25) // Amount of database hits shown per page
  const [loadedPage, setPage] = useState(1) // Current page
  const [search, setSearch] = useState(initialSearch) // Current search
  const [filters, setFilters] = useState([{ selected: '', input: [''] }]) // Current filters
  const [sorters, setSorters] = useState([{ selected: '', order: 'asc' }]) // Current sorters

  // We need to keep a reference of the columns for ranking the data
  let columns = useColumnSelection()
  let columnsRef = useRef(columns)
  let queryRef = useRef(search)

  // We update the columns if a new search is initialized
  if (search !== queryRef.current) {
    columnsRef.current = columns
    queryRef.current = search
  }

  // Current data
  const allData = useData()
  const updatedData = updateData(
    allData,
    search,
    filters,
    sorters,
    columnsRef.current
  )

  // List of variable options
  const list =
    updatedData.length > 0 &&
    Object.keys(updatedData[0]).map((item) => {
      return (
        <option key={item} value={item}>
          {item}
        </option>
      )
    })
  //the menu button to be displayed with the table
  const menu = (
    <Menu
      list={list}
      filters={filters}
      sorters={sorters}
      updateFilters={setFilters}
      updateSorters={setSorters}
    />
  )

  //main body of the page
  return (
    <>
      <Search
        tour="step-data-search"
        update={setSearch}
        initial={initialSearch}
      />
      <div tour="step-data-select" className="med-content-container">
        <h1>Data Selection Table</h1>
        <hr className="med-top-separator" />
        {TableView({
          data: updatedData,
          resultsPerPage: resultsPerPage,
          loadedPage: loadedPage,
          setPage: setPage,
          setResultsPerPage: setResultsPerPage,
          setSorters: setSorters,
          select: true,
          text: 'No data to display, please clear your search or filters.',
          menu: menu,
        })}
      </div>
    </>
  )
}

export default DataSelect
