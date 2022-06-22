// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
// this method assumes that the given input is valid

import { fetchWithToken } from '../../../../shared/api'

// creates JSON and posts the selection to the server
export default async function postSavedSelection(eunumbers, saveName) {
  var success = false

  // call to server : /api/saveselection
  const response = await fetchWithToken(
    `${process.env.PUBLIC_URL}/api/saveselection/`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: saveName,
        eunumbers: eunumbers,
      }),
    }
  )

  if (response.ok) {
    success = true
  }

  return success
}
