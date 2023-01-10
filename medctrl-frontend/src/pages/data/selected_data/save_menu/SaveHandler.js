// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import { fetchWithToken } from '../../../../shared/api'

// Handler that creates the JSON and posts the selection to the server
export default async function postSavedSelection(eu_pnumbers, saveName) {
  var success = false

  // Call to server: /api/saveselection
  const response = await fetchWithToken(
    `${process.env.PUBLIC_URL}/api/saveselection/`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: saveName,
        eu_pnumbers: eu_pnumbers,
      }),
    }
  )

  // If the response returns ok, then saving the selection
  // was successful
  if (response.ok) {
    success = true
  }

  return success
}
