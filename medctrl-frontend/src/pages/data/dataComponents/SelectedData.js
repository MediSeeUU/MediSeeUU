import React, { useState } from 'react'
import ResultsSelector from './ResultsSelector'
import Table from '../../../shared/table/table'

function SelectedData({ list }) {
  //amount of databse hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  //current page
  const [loadedPage, setPage] = useState(1)

  //all available options for resultsPerPage
  var Options = []

  //if less pages are available than the currenly loaded page, loadedPage is set to the highest available page.
  if (list.length / resultsPerPage + 1 < loadedPage) {
    setPage(list.length / resultsPerPage)
  }

  //populates the Options variable
  Options.push(
    <option key={25} value={25}>
      25
    </option>
  )
  for (var j = 50; j <= 300; j += 25) {
    Options.push(
      <option key={j} value={j}>
        {j}
      </option>
    )
  }

  //if items are selected in the select data table, these will show up here, when nothing is selected a label will be shown
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

  //main body of the page
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
