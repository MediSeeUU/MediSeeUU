// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import { fetchWithToken } from '../../../shared/api'

// Fetch and store the current saved selections
export async function fetchSavedSelections(setSavedSelections) {
  // Fetch the saved selections from the server
  const response = await fetchWithToken(
    `${process.env.PUBLIC_URL}/api/saveselection/`,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  )

  // If the response is ok, parse the JSON response and put in state
  if (response.ok) {
    const json = await response.json()
    setSavedSelections(json)
  }
}

// Delete the specified selection and set the new state
export async function fetchDeleteSelections(id, setSavedSelections) {
  // Fetch the new saved selections from the server
  const response = await fetchWithToken(
    `${process.env.PUBLIC_URL}/api/saveselection/${id}/`,
    {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  )

  // If the response is ok, parse the JSON response and put in state
  if (response.ok) {
    fetchSavedSelections(setSavedSelections)
  }
}
