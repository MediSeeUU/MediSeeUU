import { useState } from 'react'
import Table from './Table/Table'
import Paging from './Components/Paging'
import AmountPerPage from './Components/AmountPerPage'
import ClearAll from './Components/ClearAll'

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
          {!select && <ClearAll data={data} />}
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
