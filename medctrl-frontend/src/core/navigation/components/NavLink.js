// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

// Function based component that returns a nav link component
function NavLink(props) {
  const navigate = useNavigate()
  const location = useLocation()

  // If this nav link is supposed to be at the bottom of the
  // navigation bar, an extra CSS class is required
  const className = 'med-nav-item' + (props.lowest ? ' med-nav-lowest' : '')

  // If the component is the current page selected add active class
  // Do not do this if it is the lowest navlink (login)
  const active =
    location.pathname === props.dest && !props.lowest ? ' med-active' : ''

  // Click handler that closes the navigation bar
  // and redirects to the specified page
  const clicked = () => {
    props.parent.close()
    navigate(props.dest)

    // Perform extra onClick action if passed with the component
    // This is the case for logout component for example
    if (props.onClick) {
      props.onClick()
    }
  }

  return (
    <div
      className={className + ' med-primary-solid' + active}
      onClick={clicked}
      data-testid={props.name}
      role={"button"}
      tabIndex={"0"}
      onKeyPress= {(e) => {if (e.key === "Enter") clicked() }}
    >
      <div tour={props.tour} className="med-nav-item-content">
        <i className={props.image} />
        <span className="med-nav-item-name"> {props.name} </span>
      </div>
      <span className="med-nav-tooltip"> {props.name} </span>
    </div>
  )
}

export default NavLink
