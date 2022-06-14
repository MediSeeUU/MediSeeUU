//get the current saved selections
export async function fetchSavedSelections(setSavedSelections) {
  // Obtain token from session storage
  let token = sessionStorage.getItem('token')

  // Fetch the saved selections from the server
  const response = await fetch(`${process.env.PUBLIC_URL}/api/saveselection/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Token ${token}`,
    },
  })

  // If the response is ok, parse the JSON response and put in state
  if (response.ok) {
    const json = await response.json()
    setSavedSelections(json)
  }
}

//delete the selections and fetch the current selections
export async function fetchDeleteSelections(id, setSavedSelections) {
  // Obtain token from session storage
  let token = sessionStorage.getItem('token')

  // Fetch the saved selections from the server
  const response = await fetch(
    `${process.env.PUBLIC_URL}/api/saveselection/${id}`,
    {
      method: 'Delete',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Token ${token}`,
      },
    }
  )

  // If the response is ok, parse the JSON response and put in state
  if (response.ok) {
    fetchSavedSelections(setSavedSelections)
  }
}
