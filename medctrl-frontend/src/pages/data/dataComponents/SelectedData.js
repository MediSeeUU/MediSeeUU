import React, { useState } from 'react'
import TableView from './TableView'
import ExportMenu from '../ExportMenu/ExportMenu'
import SaveMenu from '../SaveMenu/SaveMenu'
import sortData from '../Utils/sorting'

function SelectedData({ selectedData }) {
  const [sorters, setSorters] = useState([{ selected: '', order: 'asc' }]) // Current sorters
  const updatedData = sortData(selectedData, [...sorters])

  //main body of the page
  return (
    <div tour="step-data-selected" className="med-content-container">
      <h1>Selected Data Points</h1>
      <hr className="med-top-separator" />
      {TableView({
        data: updatedData,
        setSorters: setSorters,
        select: false,
        text: 'No data to display, please clear your search or filters.',
        baseMenu: <ExportMenu selectedData={selectedData} />,
        saveMenu: <SaveMenu selectedData={selectedData} />,
      })}
    </div>
  )
}

export default SelectedData
