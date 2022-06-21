// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

// Login handler
async function handleLogin(event) {
  let success = false

  // Takes form and selects all items needed to send to server
  let json = {}
  event.target.querySelectorAll('input').forEach(function (item) {
    json[item.id] = item.value
  })

  // Call to server: /api/account/login/
  const response = await fetch(`${process.env.PUBLIC_URL}/api/account/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(json),
  })

  // If the response is ok, then put content in session
  if (response.ok) {
    const content = await response.json()
    setSession(content)
    success = true
  }

  return success
}

// Set session items
function setSession(res) {
  // Force the data context to fetch the most recent data by refreshing the application
  window.location.reload(false)

  sessionStorage.setItem('username', res.user.username)
  const access = res.user.groups.length > 0 ? res.user.groups[0].id : null
  sessionStorage.setItem('access_level', access)
  sessionStorage.setItem('token', res.token)
}

export default handleLogin
