// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import Toggle from './NavComponents/Toggle'
import NavLink from './NavComponents/NavLink'
import NavAccount from './NavComponents/NavAccount'
import LoginModal from '../login/LoginModal'
import React from 'react'
import OutsideClickHandler from 'react-outside-click-handler'
import './Navigation.css'
import handleLogOut from './connectionServer'

// class based compenent, represents the entire navigation side bar
class SideNavigation extends React.Component {
  // initialize the navigation bar in the collapsed position
  constructor() {
    super()

    // Get login status from sessionStorage
    let username = sessionStorage.getItem('username')
    let accessLevel = sessionStorage.getItem('access_level')
    let token = sessionStorage.getItem('token')
    let loggedin = token != null

    this.state = {
      expanded: false,
      loggedin: loggedin,
      isAdmin: false,
      userName: username,
      accessLevel: accessLevel,
    }
  }

  // sets alls parametrs to loged out
  async logOut() {
    await handleLogOut()
    this.setState({
      loggedin: false,
      isAdmin: false,
      userName: '',
      accessLevel: '',
    })
  }

  // toggles the navigation bar, if the bar is in the expanded position,
  // the navigation bar is collapsed and vice versa
  toggle() {
    this.setState({ expanded: !this.state.expanded })
  }

  // collapses the navigation bar
  close() {
    this.setState({ expanded: false })
  }

  // returns a string representation of the navigation bar state, the navigation
  // bar is either in the open (expanded) or closed (collapsed) state
  getState() {
    return this.state.expanded ? 'med-open' : 'med-closed'
  }

  // generates the entire navigation bar component, with all the appropriate elements
  render() {
    // if the user is logged in, a log out link should be rendered
    // if the user is not logged in, a log in link should be rendered
    let Auth = this.state.loggedin ? (
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

    // only if the user is logged in, a link to the account page should be rendered
    let Acc = !this.state.loggedin ? null : (
      <NavAccount
        user={{
          userName: this.state.userName,
          accessLevel: this.state.accessLevel,
        }}
        parent={this}
      />
    )

    // returns the navigation bar component, with all the appropriate elements
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
            name="Data"
            image="bx bx-data"
            dest="/data"
            parent={this}
          />
          <NavLink
            tour="step-nav-vis"
            name="Visualize"
            image="bx bx-bar-chart"
            dest="/visualizations"
            parent={this}
          />

          {Acc}
          {Auth}
        </nav>
      </OutsideClickHandler>
    )
  }
}

export default SideNavigation
