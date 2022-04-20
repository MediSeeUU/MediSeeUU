import React, { useState } from 'react'
import Menu from '../../../shared/menu/menu'
import { useData } from '../../../shared/contexts/DataContext'
import TableView from './TableView'

function DataSelect() {
  //amount of databse hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  //current page
  const [loadedPage, setPage] = useState(1)
  const allData = useData()
  const [data, setData] = useState(allData)

  //main body of the page
  return (
    <div className="TopTableHolder">
      <Menu
        cachedData={allData}
        updateTable={(updatedData) => setData(updatedData)}
      />
      {TableView(data, resultsPerPage, loadedPage, setPage, setResultsPerPage, true, "No data to display, please clear your filters.")}
    </div>
  )
}

export default DataSelect
