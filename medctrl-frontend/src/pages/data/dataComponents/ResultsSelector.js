import React, { useState } from 'react'

function ResultsSelector({
  data,
  amount,
  resultsPerPage,
  pageNumber,
  currPage,
  Options,
}) {
  
  var [lastSelected, setSelected] = useState(1);
  var pageCount = [];
  const pages = data.length / amount;
  
  
  function func(n) { 
    pageNumber(n)
    document.getElementById(lastSelected).className = 'lb-pageCount';
    document.getElementById(n).className += ' lb-pageCount_selected';
    setSelected(n);
  }
  
    //
  if (Math.ceil(pages) > 5 && currPage < 4 ) {
    pageCount.push(<div onClick={() => func(1)} className="lb-pageCount lb-pageCount_selected" id='1'> 1 </div>)

    for(var n = 2; n < 5; n++){
      pageCount.push(<div onClick={func.bind(null, n)} className="lb-pageCount" id={n}> {Math.ceil(n)} </div>)
    }

    pageCount.push(<div className="lb-pageCount"> .. </div>)

    pageCount.push(<div onClick={pageNumber.bind(null, Math.ceil(pages))} className="lb-pageCount"> {Math.ceil(pages)} </div>)
  } 
  
  if(Math.ceil(pages) > 5 && currPage >= 4  && Math.ceil(pages - 3) >= currPage){

    pageCount.push(<div onClick={pageNumber.bind(null, 1)} className="lb-pageCount"> 1 </div>)

    pageCount.push(<div className="lb-pageCount"> .. </div>)

    pageCount.push(<div onClick={pageNumber.bind(null, currPage - 1 )} className="lb-pageCount"> {currPage - 1} </div>)
    pageCount.push(<div onClick={pageNumber.bind(null, currPage)} className="lb-pageCount"> {currPage} </div>)
    pageCount.push(<div onClick={pageNumber.bind(null, currPage + 1 )} className="lb-pageCount"> {currPage + 1} </div>)

    pageCount.push(<div className="lb-pageCount"> .. </div>)

    pageCount.push(<div onClick={pageNumber.bind(null, Math.ceil(pages))} className="lb-pageCount"> {Math.ceil(pages)} </div>)
  }


  if (currPage > Math.ceil(pages - 3)) {
    pageCount.push(<div onClick={pageNumber.bind(null, 1)} className="lb-pageCount"> 1 </div>)

    pageCount.push(<div className="lb-pageCount"> .. </div>)

    for(var i = pages - 3; i <= pages; i++){
      pageCount.push(<div onClick={pageNumber.bind(null, Math.ceil(i))} className="lb-pageCount"> {Math.ceil(i)} </div>)
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
