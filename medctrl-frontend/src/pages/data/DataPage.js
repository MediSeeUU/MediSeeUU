import React, { useState } from 'react'
import Search from './Search/Search'
import DataSelect from './dataComponents/DataSelect'
import SelectedData from './dataComponents/SelectedData'
import { useData } from '../../shared/contexts/DataContext'
import './Data.css'

function DataPage() {
  const allData = useData()
  const [data, setData] = useState(allData)

  //main body of the page
  return (
    <>
      <Search data={allData} updateData={setData} />
      <DataSelect data={data} updateData={setData} />
      <SelectedData />
    </>
  )
}

export default DataPage
