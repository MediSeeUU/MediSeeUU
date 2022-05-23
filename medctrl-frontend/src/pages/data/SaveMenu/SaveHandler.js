// this method assumes that the given input is valid
// creates JSON and posts the selection to the server
async function postSavedSelection(eunumbers, saveName) {
  var success = false

  // call to server : /api/saveselection
  const response = await fetch(`${process.env.PUBLIC_URL}/api/saveselection`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: {
      name: saveName,
      eunumbers: JSON.stringify(eunumbers),
    },
  })

  if (response.status === 200) {
    success = true
  }

  return success
}
