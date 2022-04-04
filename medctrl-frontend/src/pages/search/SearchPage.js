import './SearchPage.css'
import Table from '../../shared/table/table'
import DummyData from '../../json/data.json'

function SearchPage() {

  const allData = DummyData

  return (
    <div>

      <div className="content__container__top">
        {/* <label>Active table settings</label> */}
        <button className="tableButtons">
        <i className="bx bx-cog filter-Icon"></i>Filter & Sort
        </button>
        <hr></hr>
        
        <input type="text" placeholder="Search" className='content__container__textinput' onChange={test()} />


      </div>

      <div className="content__container">
        <h1>Results</h1>

        <Table
          data={allData}
          currentPage={1}
          amountPerPage={3}
          selectTable={false}
          />
        

      </div>
    </div>
  )
}

function test() {
  console.log("test");
}

export default SearchPage
