import React, { useState , useRef} from 'react'
import { useSelectedData } from '../../../shared/contexts/DataContext'
import TableView from './TableView'
import ExportMenu from '../ExportMenu/ExportMenu'
import { useColumnSelection, useData } from '../../../shared/contexts/DataContext'
import updateData from '../Utils/update'

function SelectedData({ selectedData: allSelectedData }) {
  //amount of databse hits shown per page
  const [resultsPerPage, setResultsPerPage] = useState(25)

  //current page
  const [loadedPage, setPage] = useState(1)

  const selectedData = useSelectedData()

  let columns = useColumnSelection()
  let columnsRef = useRef(columns)
  const [search, setSearch] = useState('') // Current search
  const [filters, setFilters] = useState([{ selected: '', input: [''] }]) // Current filters
  const [sorters, setSorters] = useState([{ selected: '', order: 'asc' }]) // Current sorters
  const updatedData = updateData(
    allSelectedData,
    search,
    filters,
    sorters,
    columnsRef.current
  )


  //main body of the page
  return (
    <div tour="step-data-selected" className="med-content-container">
      <h1>Selected Data Points</h1>
      <hr className="med-top-separator" />
      {TableView({
        data: updatedData,
        resultsPerPage: resultsPerPage,
        loadedPage: loadedPage,
        setPage: setPage,
        setResultsPerPage: setResultsPerPage,
        setSorters: setSorters,
        select: false,
        text: 'No data to display, please clear your search or filters.',
        menu: <ExportMenu selectedData={selectedData} />,
      })}
    </div>
  )
}

export default SelectedData
