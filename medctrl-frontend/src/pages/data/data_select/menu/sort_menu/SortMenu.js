// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import { v4 as uuidv4 } from 'uuid'
import Sort from './Sort'

// Function based component which renders the filter menu
function SortMenu({ sorters, setSorters, defaultObj }) {
  // Add filter item to the menu
  const addSort = () => setSorters(sorters.concat(defaultObj))

  // Generic function to update the filter object
  // This is used by the other functions here
  const updateSorter = (id, func) => {
    const newSorters = sorters.map((obj, oid) => {
      if (oid === id) {
        return func(obj)
      }
      return obj
    })
    setSorters(newSorters)
  }

    // Deletes specified sort item from the menu
    const deleteSort = (id) => {
      let newSorters = [...sorters]
      newSorters.splice(id, 1)
      setSorters(newSorters)
    }

      // Updates the selected item of the specified sort item
  const updateSortSelected = (id, newSelected) => {
    updateSorter(id, (obj) => {
      return { ...obj, selected: newSelected }
    })
  }

  // Updates the sorting order of the specified sort item
  const updateSortOrder = (id, newOrder) => {
    updateSorter(id, (obj) => {
      return { ...obj, order: newOrder }
    })
  }

  return (
    <>
      <h1 className="med-table-menu-header">Sort</h1>
      <hr className="med-top-separator" />
      <div
        className="med-table-menu-add-filter med-primary-text"
        onClick={addSort}
        role={'button'}
        tabIndex={'0'}
        onKeyPress={(e) => {
          if (e.key === 'Enter') addSort()
        }}
      >
        Add Sorting option
        <i className="bx bxs-plus-square med-table-menu-add-filter-icon"></i>
      </div>
      <div className="med-table-menu-filters-container">
        {
          /* Render a Filter component for each filter in the current state
             Every filter component will receive all the functions as props to update the state */
          /* Render a Sort component for each sorter in the current state
            Every sorter component will receive all the functions as props to update the state */
            sorters.map((obj, oid) => (
              <Sort
                key={uuidv4()}
                id={oid}
                item={obj}
                del={deleteSort}
                sel={updateSortSelected}
                order={updateSortOrder}
              />
            ))
        }
      </div>
    </>
  )
}

export default SortMenu
