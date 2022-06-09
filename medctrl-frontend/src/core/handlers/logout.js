// Logout handler
async function handleLogOut() {
  // Format token string
  const token = sessionStorage.getItem('token')
  const res = 'Token ' + token

  // Call to server: /api/account/logout/
  const response = await fetch(
    `${process.env.PUBLIC_URL}/api/account/logout/`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: res },
      body: null,
    }
  )

  // If the response is ok, remove the session
  if (response.ok || response.status === 401) {
    setSession()
  }
}

// Remove session items
function setSession() {
  // force the data context to fetch the most recent data
  window.location.reload(false)

  sessionStorage.removeItem('username')
  sessionStorage.removeItem('access_level')
  sessionStorage.removeItem('token')
}

export default handleLogOut
