function Toggle(props) {
  let name = (props.expanded ? 'Collapse' : 'Expand Menu');
  let image = (props.expanded ? 'bx bx-x' : 'bx bx-menu');
  return (
    <div className='nav-item toggle' onClick={() => props.parent.toggle()}>
      <div className='nav-item-content'>
        <i className={image} />
        <span className="nav-item-name"> {name} </span>
      </div>
      <span className="tooltip"> {name} </span>
    </div>
  );
}

export default Toggle;