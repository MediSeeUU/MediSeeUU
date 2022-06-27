// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useState } from 'react'
import './SaveMenu.css'
import SaveDialog from './SaveDialog'
import MedModal from '../../../../shared/MedModal'

// Function based component, represents the save button, which is inserted
// in the selected data table. when this button is pressed, the save dialog
// compontent is shown in a react modal view
function SaveMenu({ selectedData }) {
  // Initialize the modal state
  const [showModal, setModalState] = useState(false)

  // Handlers to open and close the modal
  const openModal = () => setModalState(true)
  const closeModal = () => setModalState(false)

  return (
    <>
      <button
        className="med-primary-solid med-bx-button med-data-button"
        onClick={openModal}
      >
        <i className="bx bxs-save med-button-image"></i>Save
      </button>
      <MedModal showModal={showModal} closeModal={closeModal}>
        <SaveDialog data={selectedData} onClose={closeModal} />
      </MedModal>
    </>
  )
}

export default SaveMenu
