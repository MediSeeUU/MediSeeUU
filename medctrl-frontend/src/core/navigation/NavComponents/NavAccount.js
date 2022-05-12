import { useNavigate } from 'react-router-dom'

// function based component, returns a nav account component
// which when clicked redirects the user to the account page,
// and displays account info when the navigation is expanded
function NavAccount(props) {
  let navigate = useNavigate()
  function clicked() {
    props.parent.close()
    navigate('/account')
  }
  return (
    // when the nav account component is clicked, collapse the parent
    // (the navigation bar) and redirect the user to the account page
    <div
      className="med-primary-solid nav-item account"
      onClick={() => clicked()}
      data-testid="navaccountbutton"
    >
      <div className="nav-item-content med-primary-solid">
        <i className="bx bx-user" />
        <div>
          <span className="nav-item-name">{props.user.userName}</span>
          <br />
          <span className="nav-item-name user-alt">
            Access {props.user.accessLevel}
          </span>
        </div>
      </div>
      <span className="nav-tooltip">Account Info</span>
    </div>
  )
}

export default NavAccount
