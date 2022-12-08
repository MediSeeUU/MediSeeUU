// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import DataSelect from '../data/data_select/DataSelect'
import SelectedData from '../data/selected_data/SelectedData'
import './OrphanPage.css'
import { useSelectedData } from '../../shared/contexts/SelectedContext'

// Function based component that displays all the components on the data page
function OrphanPage() {
  const selectedData = useSelectedData()
  return (
    <>
      <DataSelect
        tableName="Orphan"
      />
      <SelectedData selectedData={selectedData} />
    </>   
  )
}

export default OrphanPage
