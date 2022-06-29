// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'

// Function based component that returns the toggle component
// which is used to expand or collapse the navigation bar
function Toggle(props) {
  // Depending on the state of the navigation bar, the toggle should
  // present the user with the right UI elements to either
  // expand or collapse the navigation bar (name of the link and the image)
  const name = props.expanded ? 'Collapse' : 'Expand Menu'
  const image = props.expanded ? 'bx bx-x' : 'bx bx-menu'

  return (
    // If the toggle is clicked, the navigation bar should to toggled
    // meaning it is either expanded or collapsed
    <div
      className="med-nav-item med-primary-solid"
      onClick={() => props.parent.toggle()}
      data-testid="navbartogglebutton"
      role={'button'}
      tabIndex={'0'}
      onKeyPress={(e) => {
        if (e.key === 'Enter') props.parent.toggle()
      }}
    >
      <div className="med-nav-item-content">
        <i className={image} />
        <span className="med-nav-item-name" data-testid="nav-item-name">
          {' '}
          {name}{' '}
        </span>
      </div>
      <span className="med-nav-tooltip"> {name} </span>
    </div>
  )
}

export default Toggle
