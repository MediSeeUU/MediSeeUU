// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useState } from 'react'
import MedModal from '../../../../shared/MedModal'
import './Menu.css'
import SortMenu from './sort_menu/SortMenu'

// Function based component which renders the filter and sort menu
function OpenSort({ sorters, update }) {
  // Default sort object
  const sortObject = [{ selected: '', order: 'asc' }]

  // Menu state variables
  const [localSorters, setSorters] = useState(sortObject)
  const [showModal, setModalState] = useState(false)

  // Handlers for opening and closing the modal
  const closeModal = () => setModalState(false)
  const openModal = () => {
    // Set current applied filters and sorters in the menu state
    setSorters(sorters)

    setModalState(true)
  }

  // Apply filters and sorters which will update the data displayed in the table and close modal
  const apply = () => {
    update(localSorters)
    closeModal()
  }

  // Clear filters and sorters which will update the data displayed in the table and close modal
  const clear = () => {
    setSorters(sortObject)
    update(sortObject)
    closeModal()
  }

  return (
    <>
      <button
        className="med-primary-solid med-bx-button med-data-button"
        onClick={openModal}
      >
        <i className="bx bx-cog med-button-image" />
        Sort
      </button>
      <MedModal
        showModal={showModal}
        closeModal={closeModal}
        className="med-table-menu-modal"
      >
        <div className="med-filter-menu">
          <SortMenu
            sorters={localSorters}
            setSorters={setSorters}
            defaultObj={sortObject}
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
      </MedModal>
    </>
  )
}

export default OpenSort
