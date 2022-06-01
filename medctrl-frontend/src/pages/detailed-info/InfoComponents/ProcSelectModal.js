import React, { useState } from 'react'
import ReactModal from 'react-modal'
import { v4 } from 'uuid'
import MedModal from '../../../shared/MedModal/MedModal'

// function based component, represents the procedure selection button, which is inserted
// in both the procedure and timeline container on the detailed info page. when this button
// is pressed, the procedure selection dialog compontent is shown in a react modal view
export default function ProcSelectModal({
  availableProcTypes,
  currentProcFilter,
  setProcFilter,
}) {
  const [showModal, setModalState] = useState(false)
  const closeModal = () => setModalState(false)

  return (
    <>
      <button
        className="med-proc-select-button med-primary-text"
        onClick={() => setModalState(true)}
      >
        Select Procedures <i className="bx bx-filter" />
      </button>

      <MedModal showModal={showModal} closeModal={closeModal}>
        <ProcSelectDialog
          closeModal={closeModal}
          availableProcTypes={availableProcTypes}
          currentProcFilter={currentProcFilter}
          setProcFilter={setProcFilter}
        />
      </MedModal>
    </>
  )
}

// function based component, it is given all the procedure types which are available for some
// medicine and it is given the current selection; which procedure types to shown and which ones
// to omit, the user can use this dialog to changes this selection. the selection can be saved
// using the apply button, or discarded using the cancel button
function ProcSelectDialog({
  closeModal,
  availableProcTypes,
  currentProcFilter,
  setProcFilter,
}) {
  const handleSubmit = (event) => {
    event.preventDefault()
    const newFilter = []
    for (let i = 0; i < availableProcTypes.length; ++i) {
      if (event.target[i] !== undefined) {
        if (event.target[i].checked) {
          newFilter.push(event.target[i].id)
        }
      }
    }
    setProcFilter(newFilter)
    closeModal()
  }

  const allOptions = availableProcTypes.map((procType) => {
    return (
      <label className="med-proc-option" key={v4()}>
        <input
          type="checkbox"
          defaultChecked={currentProcFilter.includes(procType)}
          id={procType}
        />
        <span className="med-proc-option-name">{procType}</span>
      </label>
    )
  })

  return (
    <div className="med-proc-select-dialog">
      <form onSubmit={handleSubmit}>
        <h1>Select Desired Procedure Types</h1>
        <span className="med-description">
          Below, you can select all the procedure types which should be included
          in the procedure overview and timeline on the page.
        </span>

        <div className="med-proc-option-list">{allOptions}</div>

        <button className="med-primary-solid" type="submit">
          Apply
        </button>

        <button className="med-cancel-download-button" onClick={closeModal}>
          Cancel
        </button>
      </form>
    </div>
  )
}
