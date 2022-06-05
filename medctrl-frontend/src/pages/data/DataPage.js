import React from 'react'
import DataSelect from './DataSelect/DataSelect'
import SelectedData from './SelectedData/SelectedData'
import './DataPage.css'
import { useSelectedData } from '../../shared/Context/SelectedContext'

// Data page component that displays the table components on the page
function DataPage() {
  const selectedData = useSelectedData()
  return (
    <>
      <DataSelect />
      <SelectedData selectedData={selectedData} />
    </>
  )
}

export default DataPage
