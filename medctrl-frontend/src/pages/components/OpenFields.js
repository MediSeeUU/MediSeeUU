import React, { useState } from 'react'
import MedModal from '../../shared/MedModal'
import '../data/data_select/menu/Menu.css'

// Function based component which renders the filter and sort menu
function OpenFields() {

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
        <i className="bx bx-calendar med-button-image" />
        Fields
      </button>
      <MedModal
        showModal={showModal}
        closeModal={closeModal}
        className="med-table-menu-modal"
      >
        <div className="med-changes-menu">
          <h1 className="med-table-menu-header">Fields</h1>
          <hr className="med-top-separator" />


          <div className="med-table-menu-filters-container">

          </div>


        </div>

        <div className="med-table-menu-filter-button-container">
            <button
              className="med-table-filter-button med-table-menu-secondary-button"
              onClick={closeModal}
            >
              Close
            </button>
          </div>
      </MedModal>
    </>
  )
}
export default OpenFields
