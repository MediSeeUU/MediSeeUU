// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useState } from 'react'
import TableView from '../shared/TableView'
import ExportMenu from './export_menu/ExportMenu'
import SaveMenu from './save_menu/SaveMenu'
import sortData from '../utils/sorting'

// Function based component that displays the selected datapoints
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
      { /* Only display the export menu if there is data displayed */
      updatedData.length > 0 && <ExportMenu selectedData={updatedData} />}
      { /* Only display the save menu if the user is logged in and there is data displayed */
      loggedIn && updatedData.length > 0 && (
        <SaveMenu selectedData={updatedData} />
      )}
      <hr className="med-top-separator" />
      <TableView
        data={updatedData}
        sorters={sorters}
        setSorters={setSorters}
        select={false}
        text="No data to display, please select datapoints in the table above."
      />
    </div>
  )
}

export default SelectedData
