import './SearchPage.css'
import Table from '../../shared/table/table'
import { useData } from '../../shared/contexts/DataContext'

function SearchPage() {
  const allData = useData()

  return (
    <>
      <div className="med-content-container">
        <input
          type="text"
          placeholder="Search"
          className="content__container__textinput med-text-input"
          onChange={(e) => test(e.target.value)}
        />
        <button className="med-primary-solid med-bx-button">
          <i class="bx bx-search search-Icon"></i>Search
        </button>
      </div>

      <div className="med-content-container searchDataTable">
        <h1>Search Results</h1>
        <hr className='med-top-separator'/>
        <Table
          data={allData}
          currentPage={1}
          amountPerPage={50}
          searchTable={true}
        />
      </div>
    </>
  )
}

function test(ding) {
  console.log(ding)
}

export default SearchPage
