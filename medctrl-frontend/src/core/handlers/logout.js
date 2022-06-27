// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

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
  // Force the data context to fetch the most recent data
  window.location.reload(false)

  // Remove username, access level and token from session storage
  sessionStorage.removeItem('username')
  sessionStorage.removeItem('access_level')
  sessionStorage.removeItem('token')
}

export default handleLogOut
