import Table from '../../../shared/table/table'
import ResultsSelector from './ResultsSelector'

//if items are selected in the select data table, these will show up here, when nothing is selected a label will be shown
export default function TableView({
  data,
  resultsPerPage,
  loadedPage,
  setPage,
  setResultsPerPage,
  setSorters,
  select,
  text,
  menu,
}) {
  if (!data || data.length === 0) {
    return <label className="med-table-placeholder-text">{text}</label>
  } else {
    //Maximum amount of pages available
    const amountOfPages = Math.ceil(data.length / resultsPerPage)

    //if less pages are available than the currenly loaded page, loadedPage is set to the highest available page.
    if (loadedPage > amountOfPages) {
      setPage(amountOfPages)
    }

    return (
      <>
        <Table
          data={data}
          currentPage={loadedPage}
          amountPerPage={resultsPerPage}
          selectTable={select}
          menu={menu}
          setSorters={setSorters}
        />
        <ResultsSelector
          data={data}
          amount={resultsPerPage}
          resultsPerPage={setResultsPerPage}
          pageNumber={setPage}
          currPage={loadedPage}
          clearEnabled={!select}
        />
      </>
    )
  }
}
