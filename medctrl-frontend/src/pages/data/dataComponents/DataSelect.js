import React, { useRef } from 'react'
import Menu from '../Menu/Menu'
import Search from '../../../shared/Search/Search'
import TableView from './TableView'
import {
  useData,
  useColumnSelection,
  useTableUtils,
  useTableUtilsUpdate,
} from '../../../shared/contexts/DataContext'
import updateData from '../Utils/update'

function DataSelect({ initialSearch }) {
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

  // Current data
  const allData = useData()
  const updatedData = updateData(allData, utils, columnsRef.current)

  // List of variable options
  const list =
    allData.length > 0 &&
    Object.keys(allData[0]).map((item) => {
      return (
        <option key={item} value={item}>
          {item}
        </option>
      )
    })

  //the menu button to be displayed with the table
  const menu = (
    <Menu
      list={list}
      filters={utils.filters}
      sorters={utils.sorters}
      updateFilters={(e) => utilsUpdate({ ...utils, filters: e })}
      updateSorters={(e) => utilsUpdate({ ...utils, sorters: e })}
    />
  )

  //main body of the page
  return (
    <>
      <Search
        tour="step-data-search"
        update={(e) => utilsUpdate({ ...utils, search: e })}
        initial={initialSearch || queryRef.current}
      />
      <div tour="step-data-select" className="med-content-container">
        <h1>Data Selection Table</h1>
        <hr className="med-top-separator" />
        {TableView({
          data: updatedData,
          setSorters: (e) => utilsUpdate({ ...utils, sorters: e }),
          select: true,
          text: 'No data to display, please clear your search or filters.',
          baseMenu: menu,
        })}
      </div>
    </>
  )
}

export default DataSelect
