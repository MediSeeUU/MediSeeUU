import React from 'react'
import ResultsSelector from './ResultsSelector'
import Menu from '../../../shared/menu/Menu'
import DisplayTable from '../../../shared/table/table'

import DummyData from '../../../json/small_data.json' // we can replace this with a mock API?

function DataSelect() {
  return (
    <div className="TopTableHolder">
      <Menu />
      <div className="addRmCollumn">
        <i className="bx bxs-plus-square bx-plusMinus"></i>
        <i className="bx bxs-minus-square bx-plusMinus"></i>
      </div>
      <DisplayTable data={DummyData} /> {/*all data points*/}
      <ResultsSelector />
    </div>
  )
}

export default DataSelect
