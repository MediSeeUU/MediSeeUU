import './SearchPage.css'
import Table from '../../shared/table/table'
import { useData } from '../../shared/contexts/DataContext'
import ContentContainer from '../../shared/container/ContentContainer'

function SearchPage() {
  const allData = useData()

  return (
    <div>
      <ContentContainer>
        <button className="searchbox__button">
          <i class="bx bx-search search-Icon"></i>Search
        </button>
        <input
          type="text"
          placeholder="Search"
          className="content__container__textinput"
          onChange={(e) => test(e.target.value)}
        />
      </ContentContainer>

      <ContentContainer className="searchDataTable">
        <h1>Results</h1>

        <Table
          data={allData}
          currentPage={1}
          amountPerPage={50}
          searchTable={true}
        />
      </ContentContainer>
    </div>
  )
}

function test(ding) {
  console.log(ding)
}

export default SearchPage
