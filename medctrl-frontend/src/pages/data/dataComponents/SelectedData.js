import React, { useState } from 'react'
import ResultsSelector from './ResultsSelector'
import Table from '../../../shared/table/table'

function SelectedData({ list }) {
  const [resultsPerPage, setResultsPerPage] = useState(50)
  const [loadedPage, setPage] = useState(1)

  if (list.length / resultsPerPage + 1 < loadedPage) {
    setPage(list.length / resultsPerPage)
  }

  var Options = []
  Options.push(<option value={50}>50</option>)
  for (var j = 100; j <= list.length; j += 50) {
    Options.push(<option value={j}>{j}</option>)
  }

  var tableholder
  if (!list || list.length === 0) {
    tableholder = (
      <label className="lb-tableholder">
        No data has been selected, select data points in the table above.
      </label>
    )
  } else {
    tableholder = (
      <>
        <Table
          data={list}
          currentPage={loadedPage}
          amountPerPage={resultsPerPage}
          selectedTable={true}
        />
        <ResultsSelector
          data={list}
          amount={resultsPerPage}
          resultsPerPage={setResultsPerPage}
          pageNumber={setPage}
          currPage={loadedPage}
          Options={Options}
        />
      </>
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
    </div>
  )
}

export default SelectedData
