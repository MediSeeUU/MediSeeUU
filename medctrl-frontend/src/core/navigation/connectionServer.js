//creates JSON and communicts with server
async function handleLogOut() {
  let Token = sessionStorage.getItem('token')
  let res = 'Token ' + Token

  // call to server : /api/account/logout/
  const response = await fetch(
    `${process.env.PUBLIC_URL}/api/account/logout/`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: res },
      body: null,
    }
  )

  if (response.ok || response.status === 401) {
    setSession()
  }
}

function setSession() {
  // force the data context to fetch the most recent data
  window.location.reload(false)
  sessionStorage.removeItem('username')
  sessionStorage.removeItem('access_level')
  sessionStorage.removeItem('token')
}

export default handleLogOut
