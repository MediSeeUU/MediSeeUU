import './menuitems.css'

// Returns the filter item in HTML
function displayItem(props) {
  return (
    <div id={props.id} className="sort-item">
      <select
        className="select"
        defaultValue={props.item.selected}
        onChange={(e) => props.sel(props.id, e.target.value)}
        data-testid="sort-select-attr"
      >
        <option key="" value="" hidden>
          Select a variable...
        </option>
        {props.options}
      </select>
      <select
        className="select"
        defaultValue={props.item.order}
        onChange={(e) => props.order(props.id, e.target.value)}
        data-testid="sort-select-order"
      >
        <option key="asc" value="asc">
          Ascending
        </option>
        <option key="desc" value="desc">
          Descending
        </option>
      </select>
      <i
        className="bx bxs-x-circle delete"
        data-testid="delete-sorting-box"
        onClick={() => props.del(props.id)}
      ></i>
    </div>
  )
}

export default displayItem