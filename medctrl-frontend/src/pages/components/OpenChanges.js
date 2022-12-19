// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useState } from 'react'
import MedModal from '../../shared/MedModal'
import '../data/data_select/menu/Menu.css'

// Function based component which renders the filter and sort menu
function OpenChanges({ jsonPath }) {

  const [showModal, setModalState] = useState(false)

  // Handlers for opening and closing the modal
  const closeModal = () => setModalState(false)
  const openModal = () => setModalState(true)

  return (
    <>
      <button
        className="med-primary-solid med-bx-button med-data-button"
        onClick={openModal}
      >
        <i className="bx bx-meteor med-button-image" />
        Changes
      </button>
      <MedModal
        showModal={showModal}
        closeModal={closeModal}
        className="med-table-menu-modal"
      >
        <div className="med-changes-menu">
        <h1 className="med-table-menu-header">Changes</h1>
        <hr className="med-top-separator" />
          <div className="med-table-menu-filters-container">
            <pre>
              {JSON.stringify(jsonPath, null, 2)}
            </pre>
          </div>

          <div className="med-table-menu-filter-button-container">
            <button
              className="med-table-menu-button med-table-menu-apply-button"
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

export default OpenChanges
