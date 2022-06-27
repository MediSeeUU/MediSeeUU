// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React from 'react'
import { useColumnSelection } from '../../../../../shared/contexts/ColumnSelectionContext'
import { useStructure } from '../../../../../shared/contexts/StructureContext'

// Function based component that renders the add and remove buttons for the columns
function ColumnAmount() {
  const { columnSelection, setColumnSelection } = useColumnSelection()

  // Obtain the options list
  const variableCategories = useStructure()
  const flatVars = Object.values(variableCategories).flat()
  const filteredVars = flatVars.filter(
    (variable) => variable['data-format'] !== 'link'
  )
  const options = filteredVars.map((variable) => variable['data-front-key'])

  // Handler that adds a column
  // No more columns than amount of variables can be added
  const addColumn = () => {
    let newColumnName = options.find(
      (element) => !columnSelection.includes(element)
    )
    let newColumnSelection = [...columnSelection]
    newColumnSelection.push(newColumnName)
    setColumnSelection(newColumnSelection)
  }

  // Handler that removes a column
  // There must always be 5 columns
  const removeColumn = () => {
    let newColumnSelection = [...columnSelection]
    newColumnSelection.pop()
    setColumnSelection(newColumnSelection)
  }

  return (
    <div className="med-add-remove-button-container">
      {columnSelection.length > 5 && (
        <i
          className="med-add-remove-button bx bxs-minus-square med-primary-text"
          onClick={removeColumn}
          data-testid="remove-column"
          role={"button"}
          tabIndex={"0"}
          onKeyPress= {(e) => {if (e.key === "Enter") removeColumn()}}
        />
      )}
      {columnSelection.length < options.length && (
        <i
          className="med-add-remove-button bx bxs-plus-square med-primary-text"
          onClick={addColumn}
          data-testid="add-column"
          role={"button"}
          tabIndex={"0"}
          onKeyPress= {(e) => {if (e.key === "Enter") addColumn()}}
        />
      )}
    </div>
  )
}

export default ColumnAmount
