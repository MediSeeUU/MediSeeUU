import DummyData from '../../json/data.json'
import DataSelect from './dataComponents/DataSelect'
import SelectedData from './dataComponents/SelectedData'
import { useState } from 'react'
import './Data.css'

function DataPage() {
  //State variable for the selection checkboxes, for more about states see: https://reactjs.org/docs/hooks-state.html
  const [checkedState, setCheckedState] = useState(
    Object.assign(
      {},
      ...DummyData.map((entry) => ({ [entry.EUNumber]: false }))
    )
  )

  //default filter on EU_Number
  const selectedData = DummyData.filter((item, index) => {
    return checkedState[item.EUNumber]
  })

  //main body of the page
  return (
    <div>
      <DataSelect
        setCheckedState={setCheckedState}
        checkedState={checkedState}
      />
      <SelectedData
        list={selectedData}
        setCheckedState={setCheckedState}
        checkedState={checkedState}
      />
    </div>
  )
}

export default DataPage
