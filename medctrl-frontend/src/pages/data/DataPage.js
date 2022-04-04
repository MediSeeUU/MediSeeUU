import DummyData from '../../json/data.json'
import DataSelect from './dataComponents/DataSelect'
import SelectedData from './dataComponents/SelectedData'
import { useState } from 'react'
import './Data.css'

function DataPage() {
  const allData = DummyData

  //State variable for the selection checkboxes, for more about states see: https://reactjs.org/docs/hooks-state.html
  const [checkedState, setCheckedState] = useState(
    Object.assign({}, ...allData.map((entry) => ({ [entry.EUNumber]: false })))
  )

  const selectedData = allData.filter((item, index) => {
    return checkedState[item.EUNumber]
  })

  return (
    <div>
      <DataSelect
        setCheckedState={setCheckedState}
        checkedState={checkedState}
      />
      <SelectedData list={selectedData} />
    </div>
  )
} 

export default DataPage
