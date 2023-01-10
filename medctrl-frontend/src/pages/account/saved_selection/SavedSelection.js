// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useEffect, useState } from 'react'
import { useCheckedState } from '../../../shared/contexts/CheckedContext'
import { fetchDeleteSelections } from './/savedSelectionHandlers'

// Function based component rendering a saved selection row
function SavedSelection({ savedSelection, setSavedSelection }) {
  const { checkedState, setCheckedState } = useCheckedState()

  // Create a set with the eunumbers for quicker lookup
  const selection = new Set(savedSelection.eu_pnumbers)

  // A state which describes if this saved selection is currently selected
  const [isCurrent, setIsCurrent] = useState(false)

  // Handler that updates the selection after clicking on a selection
  const updateSelection = (el) => {
    // Hard copy the checked state to re-render the selected data
    const updatedCheckedState = JSON.parse(JSON.stringify(checkedState))

    // Iterate over the eunumbers in the checked state
    for (let key of Object.keys(checkedState)) {
      // Determine if there is a match
      let match = key.match(/EU\/\d\/\d{2}\/(\d+)|(\d+)/)
      if (match) {
        // Find the eunumber and select it if it is in the selection
        const eu_pnumber = match[1] ? match[1] : match[2]
        const value = parseInt(eu_pnumber)
        updatedCheckedState[key] = selection.has(value)
      }
    }

    // Update the checked state
    setCheckedState(updatedCheckedState)

    // Set animation to select icon
    el.target.classList.add('med-animated-icon')
    setTimeout(() => {
      el.target.classList.remove('med-animated-icon')
    }, 500)
  }

  // Determines if the given json object is an empty json object
  const isEmptyObject = (obj) => {
    return (
      obj &&
      Object.keys(obj).length === 0 &&
      Object.getPrototypeOf(obj) === Object.prototype
    )
  }

  // When either the checkedState or the savedSelection changes, an evaluation
  // must be done to check if the savedSelection contains the same data points
  // as the current checkedState
  useEffect(() => {
    let match = !isEmptyObject(checkedState)
    for (let key in checkedState) {
      const isChecked = checkedState[parseInt(key)]
      const isInSelection = savedSelection.eu_pnumbers.includes(parseInt(key))

      if (isChecked !== isInSelection) {
        match = false
      }
    }
    setIsCurrent(match)
  }, [checkedState, savedSelection])

  // Describes the class name for the 'select this selection' button
  const selectClassName =
    'med-selection-select' + (isCurrent ? ' med-selected' : '')

  const date = new Date(savedSelection.created_at)
  return (
    <tr className="med-saved-selection">
      <td className="med-selection-name">{savedSelection.name}</td>
      <td className="med-selection-count">{savedSelection.eu_pnumbers.length}</td>
      <td className="med-selection-created">
        {date.toLocaleDateString()} {date.toLocaleTimeString()}
      </td>
      <td
        className={selectClassName}
        onClick={updateSelection}
        data-testid="update-select"
      >
        <i className="bx bx-select-multiple med-table-icons"></i>
      </td>
      <td
        className="med-selection-delete"
        onClick={fetchDeleteSelections.bind(
          null,
          savedSelection.id,
          setSavedSelection
        )}
        data-testid="delete-select"
      >
        <i className="bx bx-trash med-table-icons"></i>
      </td>
    </tr>
  )
}

export default SavedSelection
