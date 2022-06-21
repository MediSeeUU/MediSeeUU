// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'
import DataSelect from './data_select/DataSelect'
import SelectedData from './selected_data/SelectedData'
import './DataPage.css'
import { useSelectedData } from '../../shared/contexts/SelectedContext'

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
