import React, { useState } from 'react'
import TableView from '../shared/TableView'
import ExportMenu from './ExportMenu/ExportMenu'
import SaveMenu from './SaveMenu/SaveMenu'
import sortData from '../utils/sorting'

// Selected data component that displays the selected datapoints
function SelectedData({ selectedData }) {
  // Local sort state of the selected table
  const [sorters, setSorters] = useState([{ selected: '', order: 'asc' }])

  // Update the data based on the sorters
  const updatedData = sortData(selectedData, [...sorters])

  // Check if the user is logged in
  // Used to check if the save selection option must be displayed
  const loggedIn = sessionStorage.getItem('token') !== null

  return (
    <div tour="step-data-selected" className="med-content-container">
      <h1 className="med-header">Selected Data Points</h1>
      {loggedIn && <SaveMenu selectedData={updatedData} />}
      {updatedData.length > 0 && <ExportMenu selectedData={updatedData} />}
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
