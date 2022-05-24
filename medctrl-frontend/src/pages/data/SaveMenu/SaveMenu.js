import React, { useState } from 'react'
import ReactModal from 'react-modal'
import './SaveMenu.css'
import SaveDialog from './SaveDialog'

// function based component, represents the save button, which is inserted
// in the selected data table. when this button is pressed, the save dialog
// compontent is shown in a react modal view
function SaveMenu({ selectedData }) {
  const [showModal, setModalState] = useState(false)
  const closeModal = () => setModalState(false)

  return (
    <>
      <button
        className="med-primary-solid med-bx-button"
        onClick={() => setModalState(true)}
      >
        <i className="bx bxs-save med-button-image"></i>Save
      </button>

      <ReactModal
        className="med-save-modal"
        isOpen={showModal}
        onRequestClose={closeModal}
        ariaHideApp={false}
        style={{
          modal: {},
          overlay: {
            background: 'rgba(0, 0, 0, 0.2)',
            backdropFilter: 'blur(2px)',
          },
          content: {
            top: '50%',
            left: '50%',
            right: 'auto',
            bottom: 'auto',
            marginRight: '-50%',
            transform: 'translate(-50%, -50%)',
          },
        }}
      >
        <SaveDialog data={selectedData} onClose={closeModal} />
      </ReactModal>
    </>
  )
}

export default SaveMenu
