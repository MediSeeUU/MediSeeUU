//creates JSON and communicts with server
async function handleLogOut() {
  let Token = sessionStorage.getItem('token')
  let res = 'Token ' + Token

  // call to server : /api/account/login/
  const response = await fetch(
    `${process.env.PUBLIC_URL}/api/account/logout/`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: res },
      body: null,
    }
  )

  if (response.ok) {
    setSession()
  }
}

function setSession() {
  sessionStorage.removeItem('username')
  sessionStorage.removeItem('access_level')
  sessionStorage.removeItem('token')
}

export default handleLogOut
