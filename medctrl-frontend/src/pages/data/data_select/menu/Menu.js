// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React, { useState } from 'react'
import MedModal from '../../../../shared/MedModal'
import FilterMenu from './filter_menu/FilterMenu'
import './Menu.css'
import SortMenu from './sort_menu/SortMenu'

// Function based component which renders the filter and sort menu
function Menu({ filters, sorters, update, categories }) {
  // Default filter object
  const filterObject = [
    {
      selected: '',
      input: [{ var: '', filterRange: 'from', custom: true }],
      filterType: '',
    },
  ]

  // Default sort object
  const sortObject = [{ selected: '', order: 'asc' }]

  // Menu state variables
  const [localFilters, setFilters] = useState(filterObject)
  const [localSorters, setSorters] = useState(sortObject)
  const [showModal, setModalState] = useState(false)

  // Handlers for opening and closing the modal
  const closeModal = () => setModalState(false)
  const openModal = () => {
    // Set applied filters and sorters in the menu state
    setFilters(filters)
    setSorters(sorters)

    setModalState(true)
  }

  // Apply filters and sorters which will update the data displayed in the table and close modal
  const apply = () => {
    update(localFilters, localSorters)
    closeModal()
  }

  // Clear filters and sorters which will update the data displayed in the table and close modal
  const clear = () => {
    setFilters(filterObject)
    setSorters(sortObject)
    update(filterObject, sortObject)
    closeModal()
  }

  return (
    <>
      <button
        className="med-primary-solid med-bx-button med-data-button"
        onClick={openModal}
      >
        <i className="bx bx-cog med-button-image" />
        Filter & Sort
      </button>
      <MedModal
        showModal={showModal}
        closeModal={closeModal}
        className="med-table-menu-modal"
      >
        <div className="med-filter-menu">
          <FilterMenu
            filters={localFilters}
            setFilters={setFilters}
            defaultObj={filterObject}
            categories={categories}
          />
          <div className="med-table-menu-filter-button-container">
            <button
              className="med-table-menu-button med-table-menu-apply-button med-primary-solid"
              onClick={apply}
            >
              Apply
            </button>
            <button
              className="med-table-menu-button med-table-menu-secondary-button"
              onClick={clear}
            >
              Clear
            </button>
            <button
              className="med-table-menu-button med-table-menu-secondary-button"
              onClick={closeModal}
            >
              Close
            </button>
          </div>
        </div>
        <SortMenu
          sorters={localSorters}
          setSorters={setSorters}
          defaultObj={sortObject}
        />
      </MedModal>
    </>
  )
}

export default Menu
