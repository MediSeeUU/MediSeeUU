import { v4 as uuidv4 } from 'uuid'
import './menuitems.css'

// Returns all filter input boxes in HTML
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
          onBlur={(e) => props.fil(props.id, i, e.target.value)}
          data-testid="filter-input"
        />
        <i
          className="bx bxs-minus-circle remove-icon"
          onClick={() => props.dbox(props.id, i)}
          data-testid="remove-icon"
        ></i>
      </div>
    )
  }
  return fields
}

// Returns the filter item in HTML
function displayItem(props) {
  return (
    <div id={props.id} className="filter-item">
      <select
        className="select"
        defaultValue={props.item.selected}
        onChange={(e) => props.sel(props.id, e.target.value)}
        data-testid="filter-select"
      >
        <option key="" value="" hidden>
          Select a variable...
        </option>
        {props.options}
      </select>
      <i
        className="bx bxs-x-circle delete"
        onClick={() => props.del(props.id)}
        data-testid="delete-icon"
      ></i>
      {filtersToHTML(props)}
      <label
        id="add-label"
        onClick={() => props.box(props.id)}
        data-testid="add-label"
      >
        + Add
      </label>
    </div>
  )
}

export default displayItem
