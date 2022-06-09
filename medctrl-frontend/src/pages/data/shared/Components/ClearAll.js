import { useCheckedState } from '../../../../shared/Contexts/CheckedContext'

// Function based component that renders a clear all label
function ClearAll({ data }) {
  const { checkedState, setCheckedState } = useCheckedState()

  // Handler that removes all selected data points
  const removeAllSelected = () => {
    let updatedCheckedState = JSON.parse(JSON.stringify(checkedState))
    for (let element of data) {
      updatedCheckedState[element.EUNoShort] = false
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
