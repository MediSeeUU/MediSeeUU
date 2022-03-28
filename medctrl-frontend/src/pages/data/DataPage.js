import React, { useState } from 'react'
import './Data.css'
import DataSelect from './dataComponents/DataSelect'
import SelectedData from './dataComponents/SelectedData'


function DataPage() {
  const [data, setData] = useState(null); 

  const dataToApp = (childData) => {
    setData(childData);
  }

  return (
    <div>
      <DataSelect func={dataToApp}/> 
      <SelectedData list={data}/>
    </div>

  )
}

export default DataPage
