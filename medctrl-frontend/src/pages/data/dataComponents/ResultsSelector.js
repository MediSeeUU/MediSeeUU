import React from 'react'

function ResultsSelector({
  data,
  amount,
  resultsPerPage,
  pageNumber,
  currPage,
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
    pageCount.push(
      <div
        key={'n1'}
        onClick={() => pageNumber(1)}
        className={
          1 === currPage ? 'lb-pageCount lb-pageCount_selected' : 'lb-pageCount'
        }
        id="1"
      >
        {' '}
        1{' '}
      </div>
    )

    if (startPage > 2) {
      pageCount.push(
        <div key={'.'} className="lb-pageCount">
          {' '}
          ..{' '}
        </div>
      )

      for (var i = startPage; i <= endpage; i++) {
        pageCount.push(
          <div
            key={i}
            onClick={pageNumber.bind(null, i)}
            className={
              i === currPage
                ? 'lb-pageCount lb-pageCount_selected'
                : 'lb-pageCount'
            }
            id={i}
          >
            {' '}
            {i}{' '}
          </div>
        )
      }
    }

    if (endpage < pages - 1) {
      pageCount.push(
        <div key={'..'} className="lb-pageCount">
          {' '}
          ..{' '}
        </div>
      )
    }

    if (pages > 1) {
      pageCount.push(
        <div
          key={pages}
          onClick={() => pageNumber(pages)}
          className={
            pages === currPage
              ? 'lb-pageCount lb-pageCount_selected'
              : 'lb-pageCount'
          }
          id={pages}
        >
          {' '}
          {pages}{' '}
        </div>
      )
    }

    return pageCount
  }

  //sets currentpage to next page
  function Next() {
    if (currPage + 1 <= pages) {
      currPage += 1
    }

    pageNumber(currPage)
  }

  //sets currentpage to last page
  function Back() {
    if (currPage - 1 > 0) {
      currPage -= 1
    }

    pageNumber(currPage)
  }

  //main body of the page
  return (
    <div className="bottomOfTableHolder">
      <div className="dv-pageCount">
        <i
          onClick={() => Back()}
          className="bx bxs-chevron-left bx-plusMinus li-pageCount"
        />

        {PageSelector()}

        <i
          onClick={() => Next()}
          className="bx bxs-chevron-right bx-plusMinus li-pageCount"
        />
      </div>

      <div className="resultsSelector">
        <label>Results per page</label>
        <select
          onChange={(event) => resultsPerPage(event.target.value)}
          name="AmountShown"
          id="topSelector"
        >
          {options}
        </select>
      </div>
    </div>
  )
}

export default ResultsSelector
