import {useNavigate} from 'react-router-dom';

function NavAccount(props) {
  let navigate = useNavigate();
  function clicked() {props.parent.close(); navigate('/account'); }
  return (
    <div className='nav-item account' onClick={() => clicked()}>
      <div className='nav-item-content'>
        <i className='bx bx-user' /> 
        <div>
          <span className='nav-item-name'>{props.user.userName}</span>
          <br />
          <span className='nav-item-name user-alt'>Access {props.user.accessLevel}</span>
        </div>
      </div>
      <span className='tooltip'>Account Info</span>
    </div>
  );
}

export default NavAccount;