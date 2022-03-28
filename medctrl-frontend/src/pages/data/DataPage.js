import Table from '../../shared/table/table'
import DummyData from '../../json/data.json'

function DataPage() {
  const allData = DummyData
  let selectedData = [];

  const dataToApp = (childData) => {
    selectedData = childData;
  }
  
  return (
    <Table data={allData}
           selectTable={true}
           dataToParent={dataToApp}/>
  )
}

export default DataPage
