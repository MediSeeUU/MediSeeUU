import React from 'react'
import ResultsSelector from './ResultsSelector'
import Table from '../../../shared/table/table'

function SelectedData({ list }) {
  var tableholder
  var amountSelector
  if (!list || list.lenght === 0) {
    tableholder = <label className='lb-tableholder'>No data has been selected, select data points in the table above.</label>
    amountSelector = null;
  } else {
    tableholder = (
      <Table
        data={list}
        currentPage={1}
        amountPerPage={100}
        selectedTable={true}
      />,
      amountSelector=<ResultsSelector />
    )
  }

  return (
    <div className="TopTableHolder">
      <div>
        <label>Selected data points</label>
        <button className="tableButtons">
          <i className="bx bxs-file-export"></i>Export
        </button>
        <hr></hr>
      </div>

      {tableholder}

      {amountSelector}
    </div>
  )
}

export default SelectedData
