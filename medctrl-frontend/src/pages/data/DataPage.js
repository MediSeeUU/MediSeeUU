import Table from '../../shared/table/table'
import DummyData from '../../json/data.json'
import { useState } from 'react'

function DataPage() {
  const allData = DummyData

  //State variable for the selection checkboxes, for more about states see: https://reactjs.org/docs/hooks-state.html
  const [checkedState, setCheckedState] = useState(
    Object.assign({}, ...allData.map((entry) => ({ [entry.EUNumber]: false })))
  )

  const selectedData = allData.filter((item, index) => {
    return checkedState[item.EUNumber]
  })
//  var data = selectedData
  return (
    <Table
      data={allData}
      currentPage={2}
      amountPerPage={100}
      selectTable={true}
      setCheckedState={setCheckedState}
      checkedState={checkedState}
    />
  )
}

export default DataPage
