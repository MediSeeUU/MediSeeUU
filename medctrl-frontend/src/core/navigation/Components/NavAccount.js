import { useNavigate, useLocation } from 'react-router-dom'

// Function based component that returns a nav account component
// which also displays account info when the navigation is expanded
function NavAccount(props) {
  const navigate = useNavigate()
  const location = useLocation()

  // Click handler that closes the navigation bar
  // and redirects to the account page
  const clicked = () => {
    props.parent.close()
    navigate('/account')
  }

  const active = location.pathname === props.dest ? ' med-active' : ''

  return (
    <div
      className={'med-primary-solid med-nav-account med-nav-item' + active}
      onClick={clicked}
      data-testid="navaccountbutton"
    >
      <div className="med-nav-item-content">
        <i className="bx bx-user" />
        <div>
          <span className="med-nav-item-name">{props.user.userName}</span>
          <br />
          <span className="med-nav-item-alt-name">
            Access {props.user.accessLevel}
          </span>
        </div>
      </div>
      <span className="med-nav-tooltip">View Selections</span>
    </div>
  )
}

export default NavAccount
