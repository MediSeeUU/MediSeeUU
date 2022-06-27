// Fetches a resource from the server that needs user authentication
export function fetchWithToken(url, options) {
  // Check if user token has expired
  checkExpiry()

  // Obtain token from session storage
  let token = sessionStorage.getItem('token')

  if (token) {
    options.headers['Authorization'] = `Token ${token}`
  }

  return fetch(url, options)
}

// Checks if the user token has expired and removes the session storage items
function checkExpiry() {
  let exp = sessionStorage.getItem('token_expiry')
  if (exp) {
    let now = new Date()
    let expiry = new Date(exp)
    if (now > expiry) {
      sessionStorage.removeItem('token')
      sessionStorage.removeItem('token_expiry')
      sessionStorage.removeItem('username')
      sessionStorage.removeItem('access_level')
      window.location.reload(false)
    }
  }
}
