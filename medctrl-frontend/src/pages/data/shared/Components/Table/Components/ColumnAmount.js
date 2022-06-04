import React from 'react'
import {
  useColumnSelection,
  useColumnSelectionUpdate,
} from '../../../../../../shared/contexts/DataContext'

// Function based component that renders the add and remove buttons for the columns
function ColumnAmount({ options }) {
  const columnSelection = useColumnSelection()
  const setColumnSelection = useColumnSelectionUpdate()

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
        />
      )}
      {columnSelection.length < options.length && (
        <i
          className="med-add-remove-button bx bxs-plus-square med-primary-text"
          onClick={addColumn}
          data-testid="add-column"
        />
      )}
    </div>
  )
}

export default ColumnAmount
