import React, { useState } from 'react'
import MedModal from '../../../../shared/MedModal'
import FilterMenu from './FilterMenu/FilterMenu'
import './Menu.css'
import SortMenu from './SortMenu/SortMenu'

// Function based component which renders the filter and sort menu
function Menu({ filters, sorters, update }) {
  // Default filter object
  const filterObject = [
    {
      selected: '',
      input: [{ var: '', filterRange: 'from' }],
      filterType: '',
    },
  ]

  // Default sort object
  const sortObject = [{ selected: '', order: 'asc' }]

  // Menu state variables
  const [localFilters, setFilters] = useState(filters)
  const [localSorters, setSorters] = useState(sorters)
  const [showModal, setModalState] = useState(false)

  // Handlers for opening and closing the modal
  const closeModal = () => setModalState(false)
  const openModal = () => {
    setFilters(filters)
    setSorters(sorters)
    setModalState(true)
  }

  // Apply filters and sorters which will update the data displayed in the table
  const apply = () => {
    update(localFilters, localSorters)
    closeModal()
  }

  // Clear filters and sorters which will update the data displayed in the table
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
