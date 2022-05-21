// function based component, returns the toggle component
// used to expand or collapse the navigation bar
function Toggle(props) {
  // depending on the state of the navigation bar, the toggle should
  // present the user with the right UI elements to either
  // expand or collapse the navigation bar (name of the link and the image)
  let name = props.expanded ? 'Collapse' : 'Expand Menu'
  let image = props.expanded ? 'bx bx-x' : 'bx bx-menu'
  return (
    // when the toggle is clicked, the parent (the navigation bar) should to toggled
    // meaning it is either expanded or collapsed
    <div
      className="med-nav-item med-primary-solid"
      onClick={() => props.parent.toggle()}
      data-testid="navbartogglebutton"
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
