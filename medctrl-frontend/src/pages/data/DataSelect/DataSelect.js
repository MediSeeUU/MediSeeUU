// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React, { useRef } from 'react'
import Menu from './Menu/Menu'
import Search from '../../../shared/Search/Search'
import TableView from '../shared/TableView'
import updateData from '../utils/update'
import { useTableUtils } from '../../../shared/Contexts/TableUtilsContext'
import { useColumnSelection } from '../../../shared/Contexts/ColumnSelectionContext'
import { useData } from '../../../shared/Contexts/DataContext'

// Data select component that displays all the datapoints that can be selected
function DataSelect() {
  const { tableUtils, setTableUtils } = useTableUtils()

  // We need to keep a reference of the columns for ranking the data
  const { columnSelection } = useColumnSelection()
  let columnsRef = useRef(columnSelection)
  let queryRef = useRef(tableUtils.search)

  // We update the columns if a new search is initialized
  if (tableUtils.search !== queryRef.current) {
    columnsRef.current = columnSelection
    queryRef.current = tableUtils.search
  }

  // Update the data based on the search, filters and sorters
  const allData = useData()
  const updatedData = updateData(allData, tableUtils, columnsRef.current)

  // Handler that is called after the menu is applied
  const menuUpdate = (filters, sorters) => {
    setTableUtils({
      ...tableUtils,
      filters: filters,
      sorters: sorters,
    })
  }

  return (
    <>
      <Search
        tour="step-data-search"
        update={(e) => setTableUtils({ ...tableUtils, search: e })}
        initial={tableUtils.search}
      />
      <div tour="step-data-select" className="med-content-container">
        <h1 className="med-header">Data Selection Table</h1>
        <Menu
          filters={tableUtils.filters}
          sorters={tableUtils.sorters}
          update={menuUpdate}
        />
        <hr className="med-top-separator" />
        <TableView
          data={updatedData}
          sorters={tableUtils.sorters}
          setSorters={(e) => setTableUtils({ ...tableUtils, sorters: e })}
          select={true}
          text="No data to display, please clear your search or filters."
        />
      </div>
    </>
  )
}

export default DataSelect
