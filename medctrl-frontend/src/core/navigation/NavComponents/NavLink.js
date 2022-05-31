import { useNavigate } from 'react-router-dom'

// Function based component that returns a nav link component
function NavLink(props) {
  const navigate = useNavigate()

  // If this nav link is supposed to be at the bottom of the
  // navigation bar, an extra CSS class is required
  const className = 'med-nav-item' + (props.lowest ? ' med-nav-lowest' : '')

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
      className={className + ' med-primary-solid'}
      onClick={clicked}
      data-testid={props.name}
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
