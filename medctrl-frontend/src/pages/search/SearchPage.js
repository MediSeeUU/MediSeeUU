import './SearchPage.css'
import Table from '../../shared/table/table'
import { useData } from '../../shared/contexts/DataContext'

function SearchPage() {
  const allData = useData()

  return (
    <div>
      <div className="TopTableHolder">
        <button className="searchbox__button">
          <i className="bx bx-cog filter-Icon"></i>Filter & Sort
        </button>
        <input
          type="text"
          placeholder="Search"
          className="content__container__textinput"
          onChange={(e) => test(e.target.value)}
        />
      </div>

      <div className="TopTableHolder">
        <h1>Results</h1>

        <Table
          data={allData}
          currentPage={1}
          amountPerPage={50}
          selectTable={false}
        />
      </div>
    </div>
  )
}

function test(ding) {
  console.log(ding)
}

export default SearchPage
