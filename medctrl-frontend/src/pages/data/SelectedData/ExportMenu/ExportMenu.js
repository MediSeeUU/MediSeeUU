import React, { useState } from 'react'
import ReactModal from 'react-modal'
import './ExportMenu.css'
import ExportDialog from './ExportDialog'

// function based component, represents the export button, which is inserted
// in the selected data table. when this button is pressed, the export dialog
// compontent is shown in a react modal view
function ExportMenu({ selectedData }) {
  const [showModal, setModalState] = useState(false)
  const closeModal = () => setModalState(false)

  return (
    <>
      <button
        className="med-primary-solid med-bx-button med-data-button"
        onClick={() => setModalState(true)}
      >
        <i className="bx bxs-file-export med-button-image"></i>Export
      </button>

      <ReactModal
        className="med-export-modal"
        isOpen={showModal}
        onRequestClose={closeModal}
        ariaHideApp={false}
        style={{
          modal: {},
          overlay: {
            background: 'rgba(0, 0, 0, 0.2)',
            backdropFilter: 'blur(2px)',
          },
        }}
      >
        <ExportDialog data={selectedData} onClose={closeModal} />
      </ReactModal>
    </>
  )
}

export default ExportMenu
