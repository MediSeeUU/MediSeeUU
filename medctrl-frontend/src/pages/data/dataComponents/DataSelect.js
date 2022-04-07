import React, { useState } from 'react'
import ResultsSelector from './ResultsSelector'
import Menu from '../../../shared/menu/menu'
import Table from '../../../shared/table/table'

import allData from '../../../json/data.json' // we can replace this with a mock API?

function DataSelect({ setCheckedState, checkedState }) {
  //amount of databse hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  //current page
  const [loadedPage, setPage] = useState(1)
  const [data, setData] = useState(allData)

  //Maximum amount of pages available
  const amountOfPages = Math.ceil(data.length / resultsPerPage)

  //if less pages are available than the currenly loaded page, loadedPage is set to the highest available page.
  if (loadedPage > amountOfPages) {
    setPage(amountOfPages)
  }

  //main body of the page
  return (
    <div className="TopTableHolder">
      <Menu
        cachedData={allData}
        updateTable={(updatedData) => setData(updatedData)}
      />
      <div className="addRmCollumn">
        <i className="bx bxs-plus-square bx-plusMinus"></i>
        <i className="bx bxs-minus-square bx-plusMinus"></i>
      </div>

      <Table
        data={data}
        currentPage={loadedPage}
        amountPerPage={resultsPerPage}
        selectTable={true}
        setCheckedState={setCheckedState}
        checkedState={checkedState}
      />

      <ResultsSelector
        data={data}
        amount={resultsPerPage}
        resultsPerPage={setResultsPerPage}
        pageNumber={setPage}
        currPage={loadedPage}
      />
    </div>
  )
}

export default DataSelect
