import React, { useState } from 'react'
import MedModal from '../../shared/MedModal'
import '../data/data_select/menu/Menu.css'
import { useStructure } from '../../shared/contexts/StructureContext'
import { useColumnSelection } from '../../shared/contexts/ColumnSelectionContext'

// Function based component which renders the filter and sort menu
function OpenFields() {

  const { columnSelection, setColumnSelection } = useColumnSelection()

  // Obtain the options list
  // const variableCategories = useStructure()
  // const flatVars = Object.values(variableCategories).flat()
  // const filteredVars = flatVars.filter(
  //   (variable) => variable['data-format'] !== 'link'
  // )
  // const options = filteredVars.map((variable) => variable['data-key'])

  // // Handler that adds a column
  // // const addColumn = () => {
  // //   let newColumnName = options.find(
  // //     (element) => !columnSelection.includes(element)
  // //   )
  // //   let newColumnSelection = [...columnSelection]
  // //   newColumnSelection.push(newColumnName)
  // //   setColumnSelection(newColumnSelection)
  // // }

  //   let variables = ""



  // for (let i = 0; i < options.length; i++)
  // {
  //   variables += options[i] + ", "
  // }


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
