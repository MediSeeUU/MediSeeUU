import { useEffect, useState } from 'react'
import SavedSelection from './SavedSelection'
import DetailGroup from '../../detailed-info/Components/DetailGroup'
import './SavedSelections.css'
import { fetchSavedSelections } from './savedSelectionHandlers'

// List of saved selections
function SavedSelections() {
  // Keep a state with the saved selections
  const [savedSelections, setSavedSelections] = useState(null)

  // While rendering load in the saved selections
  useEffect(() => {
    fetchSavedSelections(setSavedSelections)
  }, [setSavedSelections])

  return (
    <div className="med-saved-selection-container">
      <DetailGroup title="Saved Selections">
        {savedSelections && savedSelections.length > 0 ? (
          <table className="med-table">
            <thead className="med-table-header">
              <tr>
                <th>Name</th>
                <th>Count</th>
                <th>Created at</th>
                <th>Select</th>
                <th>Remove</th>
              </tr>
            </thead>
            <tbody className="med-table-body">
              {savedSelections.map((x) => (
                <SavedSelection
                  key={x.id}
                  savedSelection={x}
                  setSavedSelection={setSavedSelections}
                />
              ))}
            </tbody>
          </table>
        ) : (
          <h2>No saved selections</h2>
        )}
      </DetailGroup>
    </div>
  )
}

export default SavedSelections
