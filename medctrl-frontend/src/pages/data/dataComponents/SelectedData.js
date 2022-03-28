import React from 'react'
import ResultsSelector from './ResultsSelector'

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

      <ResultsSelector />
    </div>
  )
}

export default SelectedData
