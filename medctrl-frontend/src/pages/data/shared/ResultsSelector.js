import React from 'react'
import {
  useCheckedState,
  useCheckedStateUpdate,
} from '../../../shared/contexts/DataContext'

function ResultsSelector({
  data,
  amount,
  resultsPerPage,
  setPage,
  currPage,
  clearEnabled,
}) {
  //all available options for resultsPerPage
  var options = []

  //populates the Options variable
  var upper = data.length >= 300 ? 300 : data.length

  if (data.length % 25 > 0 && data.length < 300) upper += 25

  for (var j = 25; j <= upper; j += 25) {
    options.push(
      <option key={j} value={j}>
        {j}
      </option>
    )
  }

  //pageCount holds all available pages.
  var pageCount = []

  //pages is the maximum amount of pages depnding on the amount of shown results per page
  const pages = Math.ceil(data.length / amount)

  //sets the start and end page of the results selector depending on the currently selected page
  var startPage = currPage - 1
  var endpage = currPage + 1

  if (startPage <= 1) {
    endpage -= startPage - 1
    startPage = 2
  }

  if (endpage >= pages) {
    endpage = pages - 1
    startPage = pages - 2
  }

  //populates the pageCount variable depending on the strat and end page
  function PageSelector() {
    addDiv(1)

    if (startPage > 2) {
      pageCount.push(
        <div key={'.'} className="med-table-page-button med-no-select">
          {' '}
          ..{' '}
        </div>
      )
    }

    if (pages > 3) {
      for (var i = startPage; i <= endpage; i++) {
        addDiv(i)
      }

      if (endpage < pages - 1) {
        pageCount.push(
          <div key={'..'} className="med-table-page-button med-no-select">
            {' '}
            ..{' '}
          </div>
        )
      }
    } else if (pages === 3) {
      addDiv(2)
    }

    if (pages > 1) {
      addDiv(pages)
    }

    return pageCount
  }

  //adds div with all infromation to pagecount
  function addDiv(nr) {
    pageCount.push(
      <div
        key={'nr' + nr}
        onClick={setPage.bind(null, nr)}
        className={
          nr === currPage
            ? 'med-table-page-button med-no-select med-page-selected'
            : 'med-table-page-button med-no-select'
        }
        id={nr}
      >
        {' '}
        {nr}{' '}
      </div>
    )
  }

  //sets currentpage to next page
  function Next() {
    if (currPage + 1 <= pages) {
      currPage += 1
    }

    setPage(currPage)
  }

  //sets currentpage to last page
  function Back() {
    if (currPage - 1 > 0) {
      currPage -= 1
    }

    setPage(currPage)
  }

  const checkedState = useCheckedState()
  const setCheckedState = useCheckedStateUpdate()

  //handler that removes all selected
  const removeAllSelected = () => {
    let updatedCheckedState = JSON.parse(JSON.stringify(checkedState))
    for (var element of data) {
      updatedCheckedState[element.EUNoShort] = false
    }
    setCheckedState(updatedCheckedState)
  }

  //main body of the page
  return (
    <div className="med-bottom-container-holder">
      {clearEnabled && (
        <div
          className="med-clear-all-button med-primary-text"
          onClick={removeAllSelected}
          data-testid="clear-all-label"
        >
          Clear All
          <i className="bx bxs-trash med-clear-icon"></i>
        </div>
      )}

      <div
        className="med-table-pagination-container"
        data-testid="pagination-div"
      >
        <i
          onClick={() => Back()}
          className="bx bxs-chevron-left med-table-change-page"
          data-testid="prev-page-table"
        />

        {PageSelector()}

        <i
          onClick={() => Next()}
          className="bx bxs-chevron-right med-table-change-page"
          data-testid="next-page-table"
        />
      </div>

      <div className="med-result-count-selector-container">
        <label>Results per page</label>
        <select
          onChange={(event) => resultsPerPage(event.target.value)}
          name="AmountShown"
          className="med-select"
          id="med-result-count-selector"
        >
          {options}
        </select>
      </div>
    </div>
  )
}

export default ResultsSelector
