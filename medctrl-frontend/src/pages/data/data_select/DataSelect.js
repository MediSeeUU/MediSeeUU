// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useRef, useEffect, useState } from 'react'
import Menu from './menu/Menu'
import Search from '../../../shared/search/Search'
import TableView from '../shared/TableView'
import updateData from '../utils/update'
import { useTableUtils } from '../../../shared/contexts/TableUtilsContext'
import { useColumnSelection } from '../../../shared/contexts/ColumnSelectionContext'
import { useData } from '../../../shared/contexts/DataContext'
import getUniqueCategories from '../../visualizations/single_visualization/utils/getUniqueCategories'
import ButtonComponent from '../../components/ButtonComponent.js'
import ToggleButtons from '../../components/ToggleButtons.js'
import OpenFilter from './menu/OpenFilter'
import { graphemeAt } from 'voca'
import OpenSort from './menu/OpenSort'
import * as ButtonFunctions from '../../components/ButtonFunctionality.js'
import Record from '../../components/comparison.json'
import OpenChanges from '../../components/OpenChanges'

// Function based component that displays the search bar and table with all the datapoints that can be selected
function DataSelect({ tableName }) {
  const { tableUtils, setTableUtils } = useTableUtils()

  // We need to keep a reference of the columns
  // Used in ranking the data when applying a search
  const { columnSelection } = useColumnSelection()
  let columnsRef = useRef(columnSelection)
  let queryRef = useRef(tableUtils.search)

  // We update the columns if a new search is initialized
  if (tableUtils.search !== queryRef.current) {
    columnsRef.current = columnSelection
    queryRef.current = tableUtils.search
  }

  // Update the data based on the search, filters and sorters
  // The search, filters and sorters are all located in the tableUtils context
  // Also rank the data based on the current selected columns
  const allData = useData()
  const updatedData = updateData(allData, tableUtils, columnsRef.current)

  // Handler that is called after the filters and sorters in the menu are applied
  const menuUpdate = (filters, sorters) => {
    // Update the filters and sorters context with the ones applied in the menu
    setTableUtils({
      ...tableUtils,
      filters: filters,
      sorters: sorters,
    })
  }

  // Store the categories of each variable (which are used in the filter options)
  const [categories, setCategories] = useState(null)
  useEffect(() => {
    setCategories(getUniqueCategories(allData))
  }, [allData])

  return (
    <>
      <Search
        tour="step-data-search"
        update={(e) => setTableUtils({ ...tableUtils, search: e })}
        initial={tableUtils.search}
      />
      <div tour="step-data-select" className="med-content-container">

        <ToggleButtons
          clickFunction1={ButtonFunctions.OpenHuman}
          clickFunction2={ButtonFunctions.OpenOrphan}
        />

        <hr className="med-top-separator" />
        <h1 className="med-header">Data Selection Table</h1>
        
        <OpenSort
          sorters={tableUtils.sorters}
          update={menuUpdate}
        />

        <OpenFilter
          filters={tableUtils.filters}
          update={menuUpdate}
          categories={categories}
        />

        <OpenChanges
          jsonPath={Record}
        />
        
        <ButtonComponent 
          text="Fields"
          icon="bx-calendar-plus"
          clickFunction={ButtonFunctions.FieldsMenu}
          buttonType="simple"
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
