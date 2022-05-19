import React, { useState } from 'react'
import TableView from './TableView'
import ExportMenu from '../ExportMenu/ExportMenu'

function SelectedData({ selectedData }) {
  //amount of databse hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  //current page
  const [loadedPage, setPage] = useState(1)

  //main body of the page
  return (
    <div tour="step-data-selected" className="med-content-container">
      <h1>Selected Data Points</h1>
      <hr className="med-top-separator" />
      {TableView({
        data: selectedData,
        resultsPerPage: resultsPerPage,
        loadedPage: loadedPage,
        setPage: setPage,
        setResultsPerPage: setResultsPerPage,
        select: false,
        text: 'No data to display, please clear your search or filters.',
        menu: <ExportMenu selectedData={selectedData} />,
      })}
    </div>
  )
}

export default SelectedData
