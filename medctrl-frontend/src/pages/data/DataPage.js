import React from 'react'
import DataSelect from './dataComponents/DataSelect'
import SelectedData from './dataComponents/SelectedData'
import './Data.css'
import { useSearchParams } from 'react-router-dom'
import { useSelectedData } from '../../shared/contexts/DataContext'

function DataPage() {
  // Check if the query is specified in the url parameter
  const [params] = useSearchParams()
  const query = params.get('q') || ''

  const selectedData = useSelectedData()

  //main body of the page
  return (
    <>
      <DataSelect initialSearch={query} />
      <SelectedData allSelectedData={selectedData} />
    </>
  )
}

export default DataPage
