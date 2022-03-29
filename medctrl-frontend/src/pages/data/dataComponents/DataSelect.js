import React, { useState } from 'react'
import ResultsSelector from './ResultsSelector'
import Menu from '../../../shared/menu/Menu'
import Table from '../../../shared/table/table'

import allData from '../../../json/data.json' // we can replace this with a mock API?

function DataSelect({ setCheckedState, checkedState }) {
  const [resultsPerPage, setResultsPerPage] = useState(50)
  const [loadedPage, setPage] = useState(1)

  if (allData.length / resultsPerPage + 1 < loadedPage) {
    setPage(allData.length / resultsPerPage)
  }

  var Options = []
  Options.push(<option value={50}>50</option>)
  for (var j = 100; j <= allData.length; j += 50) {
    Options.push(<option value={j}>{j}</option>)
  }

  return (
    <div className="TopTableHolder">
      <Menu />
      <div className="addRmCollumn">
        <i className="bx bxs-plus-square bx-plusMinus"></i>
        <i className="bx bxs-minus-square bx-plusMinus"></i>
      </div>

      <Table
        data={allData}
        currentPage={loadedPage}
        amountPerPage={resultsPerPage}
        selectTable={true}
        setCheckedState={setCheckedState}
        checkedState={checkedState}
      />

      <ResultsSelector
        data={allData}
        amount={resultsPerPage}
        resultsPerPage={setResultsPerPage}
        pageNumber={setPage}
        currPage={loadedPage}
        Options={Options}
      />
    </div>
  )
}

export default DataSelect
