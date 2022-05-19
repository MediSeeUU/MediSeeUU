import { v4 as uuidv4 } from 'uuid'

// Returns all filter input boxes in HTML
function filtersToHTML(props) {
  const fields = []
  for (let i = 0; i < props.item.input.length; i++) {
    fields.push(
      <div key={uuidv4()}>
        <input
          type="text"
          id={i}
          className="med-table-menu-filter-input-field med-text-input"
          defaultValue={props.item.input[i]}
          placeholder="Enter value"
          onBlur={(e) => props.fil(props.id, i, e.target.value)}
          data-testid="filter-input"
        />
        <i
          className="bx bxs-minus-circle med-table-menu-remove-filter-option-icon"
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
    <div id={props.id} className="med-table-menu-filter-item">
      <select
        className="med-table-menu-select med-select"
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
        className="bx bxs-x-circle med-table-menu-delete-button med-primary-text"
        onClick={() => props.del(props.id)}
        data-testid="delete-icon"
      ></i>
      {filtersToHTML(props)}
      <label
        className="med-table-menu-add-filter-option-button med-primary-text"
        onClick={() => props.box(props.id)}
        data-testid="add-label"
      >
        + Add
      </label>
    </div>
  )
}

export default displayItem
