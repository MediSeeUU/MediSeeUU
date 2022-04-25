import { useNavigate } from 'react-router-dom'

// function based component, returns a nav link component,
// which when clicked redirects the user to the specified page
function NavLink(props) {
  // if this nav link is supposed to be at the bottom of the
  // navigation bar, an extra css class is required
  let className = props.lowest ? 'nav-item lowest' : 'nav-item'
  let navigate = useNavigate()
  function clicked() {
    props.parent.close()
    navigate(props.dest)
  }
  return (
    // when this nav link is clicked, close the parent (the
    // navigation bar) and navigate the user to the appropriate page
    <div className={className} onClick={() => clicked()}>
      <div className="nav-item-content">
        <i className={props.image} />
        <span className="nav-item-name"> {props.name} </span>
      </div>
      <span className="nav-tooltip"> {props.name} </span>
    </div>
  )
}

export default NavLink
