import DataSelect from './dataComponents/DataSelect'
import SelectedData from './dataComponents/SelectedData'
import './Data.css'

function DataPage() {
  //main body of the page
  return (
    <div>
      <DataSelect/>
      <SelectedData/>
    </div>
  )
}

export default DataPage
