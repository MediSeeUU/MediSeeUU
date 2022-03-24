import Toggle from "./NavComponents/Toggle";
import NavLink from "./NavComponents/NavLink";
import NavAccount from "./NavComponents/NavAccount";
import React from 'react';
import OutsideClickHandler from 'react-outside-click-handler';
import './Navigation.css';

class SideNavigation extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      expanded: false,
      loggedin: props.loggedin,
      user: props.user
    }
  }

  toggle() {
    this.setState({expanded: !this.state.expanded})
  }

  close() {
    this.setState({expanded: false})
  }

  getState() {
    return (this.state.expanded ? 'open-nav' : 'closed-nav');
  }

  render() {
    let Extra = !(this.state.loggedin && this.state.user.isAdmin) ? null :
      <div>
        <hr />
        <NavLink name='Messages' image='bx bx-chat' dest='/messages' parent={this}/>
        <NavLink name='Settings' image='bx bx-cog' dest='/settings' parent={this}/>
      </div>

    let Auth = (this.state.loggedin) ? 
      <NavLink name='Logout' image='bx bx-log-out' dest='/' parent={this} lowest={true} /> :
      <NavLink name='Login' image='bx bx-log-in' dest='/' parent={this} lowest={true} />
    
    let Acc = (!this.state.loggedin) ? null : 
      <NavAccount user={this.state.user} parent={this} />

    return (
      <OutsideClickHandler onOutsideClick={() => this.close()}>
        <nav className={'side-nav ' + this.getState()}>
          <Toggle expanded={this.state.expanded} parent={this} />

          <NavLink name='Home' image='bx bx-home-alt-2' dest='/' parent={this}/>
          <NavLink name='Search' image='bx bx-search' dest='/search' parent={this}/>
          <NavLink name='Data' image='bx bx-data' dest='/data' parent={this}/>
          <NavLink name='Visualize' image='bx bx-bar-chart' dest='/visualize' parent={this}/>
          
          {Extra}          
          {Acc}
          {Auth}          
        </nav>
      </OutsideClickHandler>
    );
  }
}

export default SideNavigation;