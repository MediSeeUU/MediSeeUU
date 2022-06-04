import React, { useRef } from 'react'
import Menu from './Menu/Menu'
import Search from '../../../shared/Search/Search'
import TableView from '../shared/TableView'
import {
  useData,
  useColumnSelection,
  useTableUtils,
  useTableUtilsUpdate,
} from '../../../shared/contexts/DataContext'
import updateData from '../utils/update'

// Data select component that displays all the datapoints that can be selected
function DataSelect() {
  let utils = useTableUtils()
  let utilsUpdate = useTableUtilsUpdate()

  // We need to keep a reference of the columns for ranking the data
  let columns = useColumnSelection()
  let columnsRef = useRef(columns)
  let queryRef = useRef(utils.search)

  // We update the columns if a new search is initialized
  if (utils.search !== queryRef.current) {
    columnsRef.current = columns
    queryRef.current = utils.search
  }

  // Update the data based on the search, filters and sorters
  const allData = useData()
  const updatedData = updateData(allData, utils, columnsRef.current)

  // Handler that is called after the menu is applied
  const menuUpdate = (filters, sorters) => {
    utilsUpdate({
      ...utils,
      filters: filters,
      sorters: sorters,
    })
  }

  return (
    <>
      <Search
        tour="step-data-search"
        update={(e) => utilsUpdate({ ...utils, search: e })}
        initial={utils.search}
      />
      <div tour="step-data-select" className="med-content-container">
        <h1 className="med-header">Data Selection Table</h1>
        <Menu
          filters={utils.filters}
          sorters={utils.sorters}
          update={menuUpdate}
        />
        <hr className="med-top-separator" />
        {TableView({
          data: updatedData,
          sorters: utils.sorters,
          setSorters: (e) => utilsUpdate({ ...utils, sorters: e }),
          select: true,
          text: 'No data to display, please clear your search or filters.',
        })}
      </div>
    </>
  )
}

export default DataSelect
