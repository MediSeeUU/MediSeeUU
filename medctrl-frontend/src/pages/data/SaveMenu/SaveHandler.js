// this method assumes that the given input is valid
// creates JSON and posts the selection to the server
export default async function postSavedSelection(eunumbers, saveName) {
  var success = false

  let token = sessionStorage.getItem('token')

  // call to server : /api/saveselection
  const response = await fetch(`${process.env.PUBLIC_URL}/api/saveselection/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Token ${token}`,
    },
    body: JSON.stringify({
      name: saveName,
      eunumbers: eunumbers,
    }),
  })

  if (response.status === 200) {
    success = true
  }

  return success
}
