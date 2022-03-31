import Table from '../../shared/table/table'
import Menu from '../../shared/menu/menu'
import DummyData from '../../json/data.json'
import { useState } from 'react'

function DataPage() {
  //State variable for the selection checkboxes, for more about states see: https://reactjs.org/docs/hooks-state.html
  const [checkedState, setCheckedState] = useState(
    new Array(DummyData.length).fill(false)
  )

  const selectedData = DummyData.filter((item, index) => {
    return checkedState[index]
  })

  // Give data a state
  const [currentData, setData] = useState(DummyData)

  // Updates the state with new data and with that updating the table
  const updateTable = (updatedData) => {
    setData(updatedData)
  }

  return (
    <div>
      <Menu cachedData={DummyData} updateTable={updateTable} />
      <Table
        data={currentData}
        currentPage={1}
        amountPerPage={100}
        selectTable={true}
        setCheckedState={setCheckedState}
        checkedState={checkedState}
      />
    </div>
  )
}

export default DataPage
