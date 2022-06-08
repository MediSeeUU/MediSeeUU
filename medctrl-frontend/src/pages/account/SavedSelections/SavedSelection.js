// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import {
  useCheckedState,
  useCheckedStateUpdate,
} from '../../../shared/contexts/DataContext'

function SavedSelection({ savedSelection }) {
  const checkedState = useCheckedState()
  const setCheckedState = useCheckedStateUpdate()

  // Create a set with the eunumbers for quicker lookup
  const selection = new Set(savedSelection.eunumbers)

  const useUpdateSelection = (el) => {
    const updatedCheckedState = JSON.parse(JSON.stringify(checkedState)) //hard copy state

    for (let key of Object.keys(checkedState)) {
      let match = key.match(/EU\/\d\/\d{2}\/(\d+)|(\d+)/)
      if (match) {
        // Find the eunumbershort and select it if it is in the selection
        let eunumber = match[1] ? match[1] : match[2]
        let value = parseInt(eunumber)
        updatedCheckedState[key] = selection.has(value)
      }
    }

    setCheckedState(updatedCheckedState)
    el.target.classList.add('med-animated-icon')
    setTimeout(() => {
      el.target.classList.remove('med-animated-icon')
    }, 500)
  }

  let date = new Date(savedSelection.created_at)
  return (
    <tr className="med-saved-selection">
      <td className="med-selection-name">{savedSelection.name}</td>
      <td className="med-selection-count">{savedSelection.eunumbers.length}</td>
      <td className="med-selection-created">
        {date.toLocaleDateString()} {date.toLocaleTimeString()}
      </td>
      <td className="med-selection-count">
        <i
          onClick={useUpdateSelection.bind(null)}
          className="bx bx-select-multiple med-table-icons"
        ></i>
      </td>
    </tr>
  )
}

export default SavedSelection
