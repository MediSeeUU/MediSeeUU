import React from 'react'

function ResultsSelector({
  data,
  amount,
  resultsPerPage,
  pageNumber,
  currPage,
  Options,
}) {
  var pageCount = []

  if (Math.ceil(data.length / amount) > 5) {
    pageCount.push(
      <div onClick={pageNumber.bind(null, 1)} className="lb-pageCount">
        {' '}
        1{' '}
      </div>
    )
    pageCount.push(<div className="lb-pageCount"> .. </div>)

    for (
      var i = Math.floor((data.length / amount - 1) / 2);
      i <= Math.ceil((data.length / amount + 1) / 2);
      i++
    ) {
      pageCount.push(
        <div onClick={pageNumber.bind(null, i)} className="lb-pageCount">
          {' '}
          {i}{' '}
        </div>
      )
    }

    pageCount.push(<div className="lb-pageCount"> .. </div>)

    pageCount.push(
      <div
        onClick={pageNumber.bind(null, Math.ceil(data.length / amount))}
        className="lb-pageCount"
      >
        {' '}
        {Math.ceil(data.length / amount)}{' '}
      </div>
    )
  } else {
    for (var n = 1; n <= Math.ceil(data.length / amount); n++) {
      pageCount.push(
        <div onClick={pageNumber.bind(null, n)} className="lb-pageCount">
          {' '}
          {n}{' '}
        </div>
      )
    }
  }

  return (
    <div className="bottomOfTableHolder">
      <div className="dv-pageCount">
        <i
          onClick={() => Back(pageNumber, currPage)}
          className="bx bxs-chevron-left bx-plusMinus li-pageCount"
        />
        {pageCount}
        <i
          onClick={() =>
            Next(pageNumber, currPage, Math.ceil(data.length / amount))
          }
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
          {Options}
        </select>
      </div>
    </div>
  )
}

const Next = (pageNumber, currPage, count) => {
  var n = currPage

  if (currPage + 1 <= count) {
    n += 1
  }

  pageNumber(n)
}

const Back = (pageNumber, currPage) => {
  var n = currPage

  if (currPage - 1 > 0) {
    n -= 1
  }

  pageNumber(n)
}

export default ResultsSelector
