// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
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
      className="med-primary-solid med-nav-account med-nav-item"
      onClick={() => clicked()}
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
      <span className="med-nav-tooltip">Account Info</span>
    </div>
  )
}

export default NavAccount
