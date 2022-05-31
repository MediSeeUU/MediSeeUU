import React, { useState } from 'react'
import TableView from '../shared/TableView'
import ExportMenu from './ExportMenu/ExportMenu'
import SaveMenu from './SaveMenu/SaveMenu'
import sortData from '../utils/sorting'

function SelectedData({ selectedData }) {
  // Local sort state of the selected table
  const [sorters, setSorters] = useState([{ selected: '', order: 'asc' }])

  // Update the data based on the sorters
  const updatedData = sortData(selectedData, [...sorters])

  // Check if the user is logged in
  const loggedIn = sessionStorage.getItem('token') !== null

  return (
    <div tour="step-data-selected" className="med-content-container">
      <h1 className="med-header">Selected Data Points</h1>
      {loggedIn && <SaveMenu selectedData={selectedData} />}
      {updatedData.length > 0 && <ExportMenu selectedData={selectedData} />}
      <hr className="med-top-separator" />
      {TableView({
        data: updatedData,
        setSorters: setSorters,
        select: false,
        text: 'No data to display, please clear your search or filters.'
      })}
    </div>
  )
}

export default SelectedData
