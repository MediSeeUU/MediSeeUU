import React from 'react'
import DataSelect from './dataComponents/DataSelect'
import SelectedData from './dataComponents/SelectedData'
import './Data.css'
import { useSelectedData } from '../../shared/contexts/DataContext'

function DataPage() {
  const selectedData = useSelectedData()

  //main body of the page
  return (
    <>
      <DataSelect />
      <SelectedData selectedData={selectedData} />
    </>
  )
}

export default DataPage
