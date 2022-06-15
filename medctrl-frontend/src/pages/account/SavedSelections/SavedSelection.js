// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import { useCheckedState } from '../../../shared/Contexts/CheckedContext'
import { fetchDeleteSelections } from '../SavedSelections/savedSelectionHandlers'

// Saved selection item in the saved selections list
function SavedSelection({ savedSelection, setSavedSelection }) {
  const { checkedState, setCheckedState } = useCheckedState()

  // Create a set with the eunumbers for quicker lookup
  const selection = new Set(savedSelection.eunumbers)

  // Handler that updates the selection after clicking on a selection
  const updateSelection = (el) => {
    // Hard copy the checked state to re-render the selected data
    const updatedCheckedState = JSON.parse(JSON.stringify(checkedState))

    // Iterate over the eunumbers in the checked state
    for (let key of Object.keys(checkedState)) {
      // Determine if there is a match
      let match = key.match(/EU\/\d\/\d{2}\/(\d+)|(\d+)/)
      if (match) {
        // Find the eunumbershort and select it if it is in the selection
        const eunumber = match[1] ? match[1] : match[2]
        const value = parseInt(eunumber)
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

  const date = new Date(savedSelection.created_at)
  return (
    <tr className="med-saved-selection">
      <td className="med-selection-name">{savedSelection.name}</td>
      <td className="med-selection-count">{savedSelection.eunumbers.length}</td>
      <td className="med-selection-created">
        {date.toLocaleDateString()} {date.toLocaleTimeString()}
      </td>
      <td className="med-selection-select" onClick={updateSelection}>
        <i className="bx bx-select-multiple med-table-icons"></i>
      </td>
      <td
        className="med-selection-delete"
        onClick={fetchDeleteSelections.bind(
          null,
          savedSelection.id,
          setSavedSelection
        )}
      >
        <i className="bx bx-trash med-table-icons"></i>
      </td>
    </tr>
  )
}

export default SavedSelection
