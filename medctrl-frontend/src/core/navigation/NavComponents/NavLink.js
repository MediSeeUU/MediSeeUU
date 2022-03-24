import {useNavigate} from 'react-router-dom';

function NavLink(props) {
  let className = (props.lowest ? 'nav-item lowest' : 'nav-item');
  let navigate = useNavigate();
  function clicked() {props.parent.close(); navigate(props.dest); }
  return (
    <div className={className} onClick={() => clicked()}>
      <div className='nav-item-content'>
        <i className={props.image} />
        <span className="nav-item-name"> {props.name} </span>
      </div>
      <span className="tooltip"> {props.name} </span>
    </div>
  );
}

export default NavLink;