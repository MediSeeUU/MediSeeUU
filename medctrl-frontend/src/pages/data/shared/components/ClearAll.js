// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import { useCheckedState } from '../../../../shared/contexts/CheckedContext'

// Function based component that renders a clear all label
function ClearAll({ data }) {
  const { checkedState, setCheckedState } = useCheckedState()

  // Handler that removes all selected data points
  const removeAllSelected = () => {
    let updatedCheckedState = JSON.parse(JSON.stringify(checkedState))
    for (let element of data) {
      updatedCheckedState[element.eu_pnumber] = false
    }
    setCheckedState(updatedCheckedState)
  }

  return (
    <button
      className="med-clear-all-button med-primary-text"
      onClick={removeAllSelected}
      data-testid="clear-all-label"
    >
      Clear All <i className="bx bxs-trash"></i>
    </button>
  )
}

export default ClearAll
