import React, { useState } from 'react'
import Menu from '../../../shared/menu/menu'
import TableView from './TableView'

function DataSelect({data, updateData}) {
  //amount of database hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  //current page
  const [loadedPage, setPage] = useState(1)

  //the menu button to be displayed with the table
  const menu = (
    <Menu
      cachedData={data}
      updateTable={(updatedData) => updateData(updatedData)}
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
