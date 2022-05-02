//creates JSON and communicts with server
async function handleLogin(event) {
  var success = false

  //takes form and selects all items needed to send to server

  var json = {}
  event.target.querySelectorAll('input').forEach(function (item) {
    json[item.id] = item.value
  })

  // call to server : /api/account/login/
  const response = await fetch(`${process.env.PUBLIC_URL}/api/account/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(json),
  })

  if (response.ok) {
    const content = await response.json()

    setSession(content)
    success = true
  }

  return success
}

// sets session items
function setSession(res) {
  sessionStorage.setItem('username', res.user.username)
  let access = res.user.groups.length > 0 ? res.user.groups[0].name : null
  sessionStorage.setItem('access_level', access)
  sessionStorage.setItem('token', res.token)
}

export default handleLogin
