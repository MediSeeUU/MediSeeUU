import React from 'react'
import './Data.css'
import DataSelect from './dataComponents/DataSelect'
import SelectedData from './dataComponents/SelectedData'

function DataPage() {
  return (
    <div>
      <DataSelect />
      <SelectedData />
    </div>
  )
}

export default DataPage
