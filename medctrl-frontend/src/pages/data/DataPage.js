// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
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
