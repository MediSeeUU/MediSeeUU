import React, { useState } from 'react'
import ReactModal from 'react-modal'
import './ExportMenu.css'
import { useSelectedData } from '../../../shared/contexts/DataContext'
import ExportDialog from './ExportDialog'

// function based component, represents the export button, which is inserted
// in the selected data table. when this button is pressed, the export dialog
// compontent is shown in a react modal view
function ExportMenu() {
  const [showModal, setModalState] = useState(false)
  const selectedData = useSelectedData()

  return (
    <div>
      <button className="tableButtons" onClick={() => setModalState(true)}>
        <i className="bx bxs-file-export"></i>Export
      </button>

      <ReactModal
        className="menu-modal"
        isOpen={showModal}
        onRequestClose={() => setModalState(false)}
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
        <ExportDialog
          data={selectedData}
          onClose={() => setModalState(false)}
        />
      </ReactModal>
    </div>
  )
}

export default ExportMenu