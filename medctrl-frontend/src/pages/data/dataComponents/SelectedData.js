import React, { useState } from 'react'
import { useSelectedData } from '../../../shared/contexts/DataContext'
import TableView from './TableView'
import ExportMenu from '../ExportMenu/ExportMenu'

function SelectedData() {
  //amount of databse hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  //current page
  const [loadedPage, setPage] = useState(1)

  const selectedData = useSelectedData()

  //main body of the page
  return (
    <div className="med-content-container">
      <h1>Selected Data Points</h1>
      <hr className="med-top-separator" />
      {TableView(
        selectedData,
        resultsPerPage,
        loadedPage,
        setPage,
        setResultsPerPage,
        false,
        'No data has been selected, select data points in the table above.',
        <ExportMenu />
      )}
    </div>
  )
}

export default SelectedData
