import React, { useState } from 'react'
import Menu from '../Menu/Menu'
import Search from '../Search/Search'
import TableView from './TableView'
import { useData } from '../../../shared/contexts/DataContext'
import updateData from '../Utils/update'

function DataSelect() {
  // Amount of database hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  // Current page
  const [loadedPage, setPage] = useState(1)

  // Current search
  const [search, setSearch] = useState("")

  // Current filters
  const [filters, setFilters] = useState([{ selected: '', input: [''] }])

  // Current sorters
  const [sorters, setSorters] = useState([{ selected: '', order: 'asc' }])

  // Current data
  const allData = useData()
  const updatedData = updateData(allData, search, filters, sorters)

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
      <Search update={setSearch} />
      <div className="med-content-container">
        <h1>Data Selection Table</h1>
        <hr className="med-top-separator" />
        {TableView(
          updatedData,
          resultsPerPage,
          loadedPage,
          setPage,
          setResultsPerPage,
          true,
          'No data to display, please clear your filters.',
          menu
        )}
      </div>
    </>
  )
}

export default DataSelect
