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
      let match = key.match(/EU\/\d\/\d{2}\/(\d+)/)
      if (match) {
        // Find the eunumber and select it if it is in the selection
        let eunumber = match[1] ? match[1] : match[2]
        let value = parseInt(eunumber)
        updatedCheckedState[key] = selection.has(value)
      }
    }

    setCheckedState(updatedCheckedState)
    el.target.classList.add('animatedIcon')
    setTimeout(() => {
      el.target.classList.remove('animatedIcon')
    }, 500)
  }

  let date = new Date(savedSelection.created_at)
  return (
    <tr className="savedSelection">
      <td className="selection-name">{savedSelection.name}</td>
      <td className="selection-count">{savedSelection.eunumbers.length}</td>
      <td className="selection-created">
        {date.toLocaleDateString()} {date.toLocaleTimeString()}
      </td>
      <td className="selection-count">
        <i
          onClick={useUpdateSelection.bind(null)}
          className="bx bx-select-multiple icons"
        ></i>
      </td>
    </tr>
  )
}

export default SavedSelection
