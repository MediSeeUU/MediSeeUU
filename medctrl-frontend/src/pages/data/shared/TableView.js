// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useState } from 'react'
import Table from './table/Table'
import Paging from './components/Paging'
import AmountPerPage from './components/AmountPerPage'
import ClearAll from './components/ClearAll'

// Function based component that renders the table with its modifiers
function TableView({ data, sorters, setSorters, select, text }) {
  const [resultsPerPage, setResultsPerPage] = useState(25) // Amount of database hits shown per page
  const [loadedPage, setPage] = useState(1) // Current page

  // If there is data to display, it will show the table, otherwise a label will be shown
  if (!data || data.length === 0) {
    return <label className="med-table-placeholder-text">{text}</label>
  } else {
    // Maximum amount of pages available
    const amountOfPages = Math.ceil(data.length / resultsPerPage)

    // If less pages are available than the currently loaded page, loadedPage is set to the highest available page
    if (loadedPage > amountOfPages) {
      setPage(amountOfPages)
    }

    return (
      <>
        <Table
          data={data}
          currentPage={loadedPage}
          amountPerPage={resultsPerPage}
          select={select}
          sorters={sorters}
          setSorters={setSorters}
        />
        <div className="med-bottom-container-holder">
          { /* Only show the clear all icon if it is a table with selected datapoints */
          !select && <ClearAll data={data} />}
          <Paging
            data={data}
            amount={resultsPerPage}
            currPage={loadedPage}
            setPage={setPage}
          />
          <AmountPerPage data={data} resultsPerPage={setResultsPerPage} />
        </div>
      </>
    )
  }
}

export default TableView
