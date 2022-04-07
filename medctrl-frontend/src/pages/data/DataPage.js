import DataSelect from './dataComponents/DataSelect'
import SelectedData from './dataComponents/SelectedData'
import './Data.css'
import { useSelectedData } from '../../shared/datacontext/DataContext'

function DataPage() {
  const selectedData = useSelectedData();
  //main body of the page
  return (
    <div>
      <DataSelect/>
      <SelectedData
        list={selectedData}
      />
    </div>
  )
}

export default DataPage
