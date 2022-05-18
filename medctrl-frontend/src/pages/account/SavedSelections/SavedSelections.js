import { useEffect, useState } from 'react'
import SavedSelection from './SavedSelection'
import DetailGroup from '../../detailed-info/InfoComponents/DetailGroup'
import './SavedSelections.css'

export default function SavedSelections(props) {
  const [savedSelections, setsavedSelections] = useState(null)

  useEffect(() => {
    // Fetch the saved selections from the server
    async function fetchSavedSelections() {
      let token = sessionStorage.getItem('token')

      const response = await fetch(
        `${process.env.PUBLIC_URL}/api/saveselection`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token}`,
          },
        }
      )

      const data = await response.json()
      setsavedSelections(data)
    }
    fetchSavedSelections()
  }, [setsavedSelections])

  return (
    <div>
      <DetailGroup title="Saved Selections">
        {savedSelections && savedSelections.length > 0 ? (
          <table className="med_table">
            <thead className="tableHeader">
              <tr>
                <th>Name</th>
                <th>Count</th>
                <th>Created at</th>
                <th>Select</th>
              </tr>
            </thead>
            <tbody className="tableBody">
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
