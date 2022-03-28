import './MenuItem.css';

function displayItem(props) {
  return(
    <div key={props.id} className="MenuItem">
      <select id="filterSelect" defaultValue={props.selected} onChange={e => props.update(props.id, e.target.value, true)}>{props.options}</select>
      <i className="bx bxs-x-circle delete" onClick={() => props.del(props.id)}></i>
      <input type="text" id="filterInput" defaultValue={props.input} placeholder={"Enter value"} onChange={e => props.update(props.id, e.target.value, false)}/>
      <label id="addLabel" onClick={props.add}>+ Add filter</label>
    </div>
  );
}

export default displayItem;
