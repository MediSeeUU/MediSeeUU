import React, { useState } from 'react'
import ResultsSelector from './ResultsSelector'
import Menu from '../../../shared/menu/Menu'
import Table from '../../../shared/table/table'

import allData from '../../../json/data.json' // we can replace this with a mock API?

function DataSelect({ setCheckedState, checkedState }) {
  //amount of databse hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  //current page
  const [loadedPage, setPage] = useState(1)

  //all available options for resultsPerPage
  var Options = []

  //if less pages are available than the currenly loaded page, loadedPage is set to the highest available page.
  if (allData.length / resultsPerPage + 1 < loadedPage) {
    setPage(allData.length / resultsPerPage)
  }

  //populates the Options variable
  Options.push(<option  key={25} value={25}>25</option>)
  for (var j = 50; j <= 300; j += 25) {
    Options.push(<option key={j} value={j}>{j}</option>)
  }

  //main body of the page
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
