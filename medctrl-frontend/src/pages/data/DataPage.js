import Table from '../../shared/table/table'
import DummyData from '../../json/data.json'

function DataPage() {
  const allData = DummyData
  let selectedData = []

  const dataToApp = (childData) => {
    selectedData = childData
  }

  return (
    <Table
      data={allData}
      currentPage={1}
      amountPerPage={100}
      selectTable={true}
      dataToParent={dataToApp}
    />
  )
}

export default DataPage
