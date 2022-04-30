import React, { useState } from 'react'
import Search from './Search/Search'
import DataSelect from './dataComponents/DataSelect'
import SelectedData from './dataComponents/SelectedData'
import { useData } from '../../shared/contexts/DataContext'
import updateData from './Utils/update'
import './Data.css'

function DataPage() {
  const [search, setSearch] = useState("")

  const [filters, setFilters] = useState([{ selected: '', input: [''] }])
  const [sorters, setSorters] = useState([{ selected: '', order: 'asc' }])

  const allData = useData()
  const updatedData = updateData(allData, search, filters, sorters)

  //main body of the page
  return (
    <>
      <Search update={setSearch} />
      <DataSelect data={updatedData} filters={filters} sorters={sorters} updateFilters={setFilters} updateSorters={setSorters} />
      <SelectedData />
    </>
  )
}

export default DataPage
