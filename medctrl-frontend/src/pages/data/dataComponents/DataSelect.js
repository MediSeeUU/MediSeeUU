import React from 'react'
import ResultsSelector from './ResultsSelector'
import Menu from '../../../shared/menu/Menu'
import Table from '../../../shared/table/table'

import allData from '../../../json/small_data.json' // we can replace this with a mock API?

function DataSelect({func}) {
  return (
    <div className="TopTableHolder">
      <Menu />
      <div className="addRmCollumn">
        <i className="bx bxs-plus-square bx-plusMinus"></i>
        <i className="bx bxs-minus-square bx-plusMinus"></i>
      </div>

      <Table
        data={allData}
        currentPage={1}
        amountPerPage={100}
        selectTable={true}
        dataToParent={func}
      />

      <ResultsSelector />
    </div>
  )
}

export default DataSelect
