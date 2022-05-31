import { useEffect, useState } from 'react'
import SavedSelection from './SavedSelection'
import DetailGroup from '../../detailed-info/InfoComponents/DetailGroup'
import './SavedSelections.css'

// List of saved selections
function SavedSelections() {
  // Keep a state with the saved selections
  const [savedSelections, setSavedSelections] = useState(null)

  // While rendering load in the saved selections
  useEffect(() => {
    async function fetchSavedSelections() {
      // Obtain token from session storage
      let token = sessionStorage.getItem('token')

      // Fetch the saved selections from the server
      const response = await fetch(
        `${process.env.PUBLIC_URL}/api/saveselection/`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token}`,
          },
        }
      )

      // If the response is ok, parse the JSON response and put in state
      if (response.ok) {
        const json = await response.json()
        setSavedSelections(json)
      }
    }
    fetchSavedSelections()
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
              </tr>
            </thead>
            <tbody className="med-table-body">
              {savedSelections.map((x) => (
                <SavedSelection key={x.id} savedSelection={x} />
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
