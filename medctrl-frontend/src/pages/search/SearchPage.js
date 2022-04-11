import './SearchPage.css'
import Table from '../../shared/table/table'
import DummyData from '../../json/data.json'

function SearchPage() {
  const allData = DummyData

  return (
    <div>
      <div className="TopTableHolder">
        <button className="searchbox__button">
          <i class="bx bx-search search-Icon"></i>Search
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
          searchTable={true}
        />
      </div>
    </div>
  )
}

function test(ding) {
  console.log(ding)
}

export default SearchPage
