// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import Toggle from './components/Toggle'
import NavLink from './components/NavLink'
import NavAccount from './components/NavAccount'
import LoginModal from '../login/LoginModal'
import OutsideClickHandler from 'react-outside-click-handler'
import './Navigation.css'
import handleLogOut from '../handlers/logout'

// Class based component rendering the entire navigation side bar
// Because of the extensive state, we use a class instead of a function based component here
class SideNavigation extends React.Component {
  // Initialize the navigation bar in the collapsed position
  constructor(props) {
    super(props)

    // Get login status from session storage
    let username = sessionStorage.getItem('username')
    let accessLevel = sessionStorage.getItem('access_level')
    let token = sessionStorage.getItem('token')
    let loggedIn = token !== null

    // Set the default state
    this.state = {
      expanded: false,
      loggedIn: loggedIn,
      isAdmin: false,
      userName: username,
      accessLevel: accessLevel,
    }
  }

  // Calls logout handler and updates local state
  async logOut() {
    await handleLogOut()
    this.setState({
      loggedIn: false,
      isAdmin: false,
      userName: '',
      accessLevel: '',
    })
  }

  // Toggles the navigation bar, if the bar is in the expanded position,
  // the navigation bar is collapsed and vice versa
  toggle() {
    this.setState({ expanded: !this.state.expanded })
  }

  // Collapses the navigation bar
  close() {
    this.setState({ expanded: false })
  }

  // Returns a string representation of the navigation bar state, the navigation
  // bar is either in the open (expanded) or closed (collapsed) state
  getState() {
    return this.state.expanded ? 'med-open' : 'med-closed'
  }

  // Renders the navigation bar
  render() {
    // If the user is logged in, a log out link should be rendered
    // If the user is not logged in, a log in link should be rendered
    const authenticated = this.state.loggedIn ? (
      <NavLink
        name="Logout"
        image="bx bx-log-out"
        dest="/"
        parent={this}
        lowest={true}
        onClick={this.logOut.bind(this)}
      />
    ) : (
      <LoginModal parent={this} />
    )

    // Only if the user is logged in, a link to the account page should be rendered
    const account = this.state.loggedIn && (
      <NavAccount
        user={{
          userName: this.state.userName,
          accessLevel: this.state.accessLevel,
        }}
        dest="/account"
        parent={this}
      />
    )

    // Returns the navigation bar component, with all the appropriate elements
    return (
      <OutsideClickHandler onOutsideClick={this.close.bind(this)}>
        <nav className={'med-side-nav ' + this.getState()}>
          <Toggle expanded={this.state.expanded} parent={this} />
          <NavLink
            tour="step-nav-home"
            name="Home"
            image="bx bx-home-alt-2"
            dest="/"
            parent={this}
          />
          <NavLink
            name="Info"
            image="bx bx-info-circle"
            dest="/info"
            parent={this}
          />
          <NavLink
            tour="step-nav-data"
            name="Human"
            image="bx bx-data"
            dest="/data"
            parent={this}
          />
          <NavLink
            tour="step-nav-data"
            name="Orphan"
            image="bx bx-data"
            dest="/orphan"
            parent={this}
          />
          <NavLink
            tour="step-nav-vis"
            name="Visualize"
            image="bx bx-bar-chart"
            dest="/visualizations"
            parent={this}
          />
          {account}
          {authenticated}
        </nav>
      </OutsideClickHandler>
    )
  }
}

export default SideNavigation
