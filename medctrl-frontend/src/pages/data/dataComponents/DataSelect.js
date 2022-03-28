import React from 'react'
import ResultsSelector from './ResultsSelector'
import Menu from '../../../shared/menu/Menu'

function DataSelect() {
  return (
    <div className="TopTableHolder">
      <Menu />

      <div className="addRmCollumn">
        <i className="bx bxs-plus-square bx-plusMinus"></i>
        <i className="bx bxs-minus-square bx-plusMinus"></i>
      </div>

      <ResultsSelector />
    </div>
  )
}

export default DataSelect
