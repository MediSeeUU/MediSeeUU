// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import { useEffect, useState } from 'react'
import SavedSelection from './SavedSelection'
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
    </div>
  )
}

export default SavedSelections
