import React, { useState } from 'react'
import Menu from '../Menu/Menu'
import TableView from './TableView'

function DataSelect({data, filters, sorters, updateFilters, updateSorters}) {
  //amount of database hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  //current page
  const [loadedPage, setPage] = useState(1)

  // List of variable options
  const list =
    data.length > 0 &&
    Object.keys(data[0]).map((item) => {
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
      updateFilters={updateFilters}
      updateSorters={updateSorters}
    />
  )

  //main body of the page
  return (
    <div className="med-content-container">
      <h1>Data Selection Table</h1>
      <hr className="med-top-separator" />
      {TableView(
        data,
        resultsPerPage,
        loadedPage,
        setPage,
        setResultsPerPage,
        true,
        'No data to display, please clear your filters.',
        menu
      )}
    </div>
  )
}

export default DataSelect
