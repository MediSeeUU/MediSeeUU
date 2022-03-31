import { v4 as uuidv4 } from 'uuid'
import './MenuItem.css'

function filtersToHTML(props) {
  const fields = []
  for (let i = 0; i < props.item.input.length; i++) {
    fields.push(
      <div key={uuidv4()}>
        <input
          type="text"
          id={i}
          className="filter-input"
          defaultValue={props.item.input[i]}
          placeholder="Enter value"
          onBlur={(e) => props.fil(props.id, e.target.id, e.target.value)}
        />
        <i
          className="bx bxs-minus-circle remove-icon"
          onClick={() => props.dbox(props.id, i)}
        ></i>
      </div>
    )
  }
  return fields
}

function displayItem(props) {
  return (
    <div id={props.id} className="menu-item">
      <select
        id="filter-select"
        defaultValue={props.item.selected}
        onChange={(e) => props.sel(props.id, e.target.value)}
      >
        <option key="" value="" hidden>
          Select a variable...
        </option>
        {props.options}
      </select>
      <i
        className="bx bxs-x-circle delete"
        onClick={() => props.del(props.id)}
      ></i>
      {filtersToHTML(props)}
      <label id="add-label" onClick={() => props.box(props.id)}>
        + Add
      </label>
    </div>
  )
}

export default displayItem
