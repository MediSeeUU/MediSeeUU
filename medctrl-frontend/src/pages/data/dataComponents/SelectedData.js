import React, { useState } from 'react'
import { useSelectedData } from '../../../shared/contexts/DataContext'
import TableView from './TableView'

function SelectedData() {
  //amount of databse hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  //current page
  const [loadedPage, setPage] = useState(1)

  const selectedData = useSelectedData()

  //main body of the page
  return (
    <div className="TopTableHolder">
      <div>
        <label>Selected data points</label>
        <button className="tableButtons">
          <i className="bx bxs-file-export"></i>Export
        </button>
        <hr></hr>
      </div>
      {TableView(
        selectedData,
        resultsPerPage,
        loadedPage,
        setPage,
        setResultsPerPage,
        false,
        'No data has been selected, select data points in the table above.'
      )}
    </div>
  )
}

export default SelectedData
