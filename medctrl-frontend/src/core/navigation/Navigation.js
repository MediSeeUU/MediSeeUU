import Toggle from './NavComponents/Toggle'
import NavLink from './NavComponents/NavLink'
import NavAccount from './NavComponents/NavAccount'
import React from 'react'
import OutsideClickHandler from 'react-outside-click-handler'
import './Navigation.css'

// class based compenent, represents the entire navigation side bar
class SideNavigation extends React.Component {
  // initialize the navigation bar in the collapsed position
  constructor(props) {
    super(props)
    this.state = {
      expanded: false,
      loggedin: props.loggedin,
      user: props.user,
    }
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
    return this.state.expanded ? 'open-nav' : 'closed-nav'
  }

  // generates the entire navigation bar component, with all the appropriate elements
  render() {
    // if a user is logged in and is an admin, display the links to the
    // messages and settings pages below the other links
    let Extra = !(this.state.loggedin && this.state.user.isAdmin) ? null : (
      <div>
        <hr className="nav-separator" />
        <NavLink
          name="Messages"
          image="bx bx-chat"
          dest="/messages"
          parent={this}
        />
        <NavLink
          name="Settings"
          image="bx bx-cog"
          dest="/settings"
          parent={this}
        />
      </div>
    )

    // if the user is logged in, a log out link should be rendered
    // if the user is not logged in, a log in link should be rendered
    let Auth = this.state.loggedin ? (
      <NavLink
        name="Logout"
        image="bx bx-log-out"
        dest="/"
        parent={this}
        lowest={true}
      />
    ) : (
      <NavLink
        name="Login"
        image="bx bx-log-in"
        dest="/"
        parent={this}
        lowest={true}
      />
    )

    // only if the user is logged in, a link to the account page should be rendered
    let Acc = !this.state.loggedin ? null : (
      <NavAccount user={this.state.user} parent={this} />
    )

    // returns the navigation bar component, with all the appropriate elements
    return (
      <OutsideClickHandler onOutsideClick={() => this.close()}>
        <nav className={'side-nav ' + this.getState()}>
          <Toggle expanded={this.state.expanded} parent={this} />

          <NavLink
            name="Home"
            image="bx bx-home-alt-2"
            dest="/"
            parent={this}
          />
          <NavLink
            name="Search"
            image="bx bx-search"
            dest="/search"
            parent={this}
          />
          <NavLink name="Data" image="bx bx-data" dest="/data" parent={this} />
          <NavLink
            name="Visualize"
            image="bx bx-bar-chart"
            dest="/visualizations"
            parent={this}
          />

          {Extra}
          {Acc}
          {Auth}
        </nav>
      </OutsideClickHandler>
    )
  }
}

export default SideNavigation
