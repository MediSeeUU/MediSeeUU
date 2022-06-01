import React, { useState } from 'react'
import './SaveMenu.css'
import SaveDialog from './SaveDialog'
import MedModal from '../../../../shared/MedModal/MedModal'

// function based component, represents the save button, which is inserted
// in the selected data table. when this button is pressed, the save dialog
// compontent is shown in a react modal view
function SaveMenu({ selectedData }) {
  const [showModal, setModalState] = useState(false)
  const closeModal = () => setModalState(false)

  return (
    <>
      <button
        className="med-primary-solid med-bx-button med-data-button"
        onClick={() => setModalState(true)}
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
