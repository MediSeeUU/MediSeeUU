// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'
import { v4 as uuidv4 } from 'uuid'
import Filter from './Filter'

// Function based component which renders the filter menu
function FilterMenu({ filters, setFilters, defaultObj, categories }) {
  // Add filter item to the menu
  const addFilter = () => setFilters(filters.concat(defaultObj))

  // Generic function to update the filter object
  // This is used by the other functions here
  const updateFilter = (id, func) => {
    const newFilters = filters.map((obj, oid) => {
      if (oid === id) {
        return func(obj)
      }
      return obj
    })
    setFilters(newFilters)
  }

  // Add a filter box to the specified filter item
  const addFilterBox = (id) => {
    updateFilter(id, (obj) => {
      const newInput = obj.input.concat({ var: '', filterRange: 'from', custom: true })
      return { ...obj, input: newInput }
    })
  }

  // Deletes the specified input box of the filter item
  const deleteFilterBox = (id, bid) => {
    updateFilter(id, (obj) => {
      if (obj.input.length > 1) {
        let newInput = [...obj.input]
        newInput.splice(bid, 1)
        return { ...obj, input: newInput }
      }
      return { ...obj, input: [{ var: '', filterRange: 'from', custom: true }] }
    })
  }

  // Deletes specified filter item from the menu
  const deleteFilter = (id) => {
    let newFilters = [...filters]
    newFilters.splice(id, 1)
    setFilters(newFilters)
  }

  // Updates the selected item of the specified filter item
  const updateFilterSelected = (id, newSelected) => {
    updateFilter(id, (obj) => {
      return { ...obj, selected: newSelected }
    })
  }

  // Updates the specified input box value of the specified filter item
  const updateFilterInput = (id, bid, newValue) => {
    updateFilter(id, (obj) => {
      let newInput = [...obj.input]
      newInput[bid].var = newValue
      return { ...obj, input: newInput }
    })
  }

  return (
    <>
      <h1 className="med-table-menu-header">Filters</h1>
      <hr className="med-top-separator" />
      <div
        className="med-table-menu-add-filter med-primary-text"
        onClick={addFilter}
      >
        Add Filter
        <i className="bx bxs-plus-square med-table-menu-add-filter-icon"></i>
      </div>
      <div className="med-table-menu-filters-container">
        {filters.map((filter, index) => (
          <Filter
            key={uuidv4()}
            id={index}
            item={filter}
            del={deleteFilter}
            box={addFilterBox}
            dbox={deleteFilterBox}
            sel={updateFilterSelected}
            fil={updateFilterInput}
            cats={categories}
          />
        ))}
      </div>
    </>
  )
}

export default FilterMenu
