import React, { useState } from 'react'
import ResultsSelector from './ResultsSelector'
import Menu from '../../../shared/menu/menu'
import Table from '../../../shared/table/table'
import { useData } from '../../../shared/contexts/DataContext'

function DataSelect() {

  //amount of databse hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  //current page
  const [loadedPage, setPage] = useState(1)
  const allData = useData()
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

      <Table
        data={data}
        currentPage={loadedPage}
        amountPerPage={resultsPerPage}
        selectTable={true}
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
