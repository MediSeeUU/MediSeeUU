import React from 'react'
import ResultsSelector from './ResultsSelector'
import DisplayTable from '../../../shared/table/table'

import DummyData from '../../../json/small_data.json' // we can replace this with a mock API?

function SelectedData() {
  return (
    <div className="TopTableHolder">
      <div>
        <label>Selected data points</label>
        <button className="tableButtons">
          <i className="bx bxs-file-export"></i>Export
        </button>
        <hr></hr>
      </div>
      <DisplayTable data={DummyData} />
      <ResultsSelector />
    </div>
  )
}

export default SelectedData
