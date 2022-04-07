import React, { useState } from 'react'
import ResultsSelector from './ResultsSelector'
import Table from '../../../shared/table/table'
import { useSelectedData } from '../../../shared/datacontext/DataContext'

function SelectedData() {
  //amount of databse hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  //current page
  const [loadedPage, setPage] = useState(1)

  const selectedData = useSelectedData();
  //if items are selected in the select data table, these will show up here, when nothing is selected a label will be shown
  var tableholder
  if (!selectedData || selectedData.length === 0) {
    tableholder = (
      <label className="lb-tableholder">
        No data has been selected, select data points in the table above.
      </label>
    )
  } else {
    //Maximum amount of pages available
    const amountOfPages = Math.ceil(selectedData.length / resultsPerPage)

    //if less pages are available than the currenly loaded page, loadedPage is set to the highest available page.
    if (loadedPage > amountOfPages) {
      setPage(amountOfPages)
    }

    tableholder = (
      <>
        <Table
          data={selectedData}
          currentPage={loadedPage}
          amountPerPage={resultsPerPage}
          selectedTable={true}
        />
        <ResultsSelector
          data={selectedData}
          amount={resultsPerPage}
          resultsPerPage={setResultsPerPage}
          pageNumber={setPage}
          currPage={loadedPage}
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
