// Function based component that displays the paging of the table
function Paging({ data, amount, currPage, setPage }) {
  // Holds all available pages
  let paging = []

  // Maximum amount of pages depending on the amount of shown results per page
  const pages = Math.ceil(data.length / amount)

  // Set start and end page of the results selector depending on the currently selected page
  let startPage = currPage - 1
  let endpage = currPage + 1

  if (startPage <= 1) {
    endpage -= startPage - 1
    startPage = 2
  }

  if (endpage >= pages) {
    endpage = pages - 1
    startPage = pages - 2
  }

  // Populates the paging with the pages
  const pageSelector = () => {
    // Always add page 1
    addPage(1)

    // If the startpage is greater than two, add dots to at the start
    if (startPage > 2) {
      paging.push(
        <div key={'.'} className="med-table-page-button med-no-select">
          {' '}
          ..{' '}
        </div>
      )
    }

    // If the amount of pages is greater than three, add the pages between the dots
    if (pages > 3) {
      for (let i = startPage; i <= endpage; i++) {
        addPage(i)
      }

      // Only add dots at the end if last visible page is three pages away from the last page
      if (endpage < pages - 1) {
        paging.push(
          <div key={'..'} className="med-table-page-button med-no-select">
            {' '}
            ..{' '}
          </div>
        )
      }
      // If the amount of pages is exactly three, then only add page 2
    } else if (pages === 3) {
      addPage(2)
    }

    // Add the last page if the amount of pages is greater than one
    if (pages > 1) {
      addPage(pages)
    }

    return paging
  }

  // Generic function to add page number
  const addPage = (page) => {
    paging.push(
      <div
        key={'page' + page}
        onClick={setPage.bind(null, page)}
        className={
          page === currPage
            ? 'med-table-page-button med-no-select med-page-selected'
            : 'med-table-page-button med-no-select'
        }
        id={page}
      >
        {' '}
        {page}{' '}
      </div>
    )
  }

  // Set current page to next page
  const next = () => {
    // Only update current page if it does not go beyond the last page
    if (currPage + 1 <= pages) {
      currPage += 1
    }
    setPage(currPage)
  }

  // Set current page to previous page
  const back = () => {
    // Only update current page if it does not go lower than one
    if (currPage - 1 > 0) {
      currPage -= 1
    }
    setPage(currPage)
  }

  return (
    <div
      className="med-table-pagination-container"
      data-testid="pagination-div"
    >
      <i
        onClick={back}
        className="bx bxs-chevron-left med-table-change-page"
        data-testid="prev-page-table"
      />
      {pageSelector()}
      <i
        onClick={next}
        className="bx bxs-chevron-right med-table-change-page"
        data-testid="next-page-table"
      />
    </div>
  )
}

export default Paging
