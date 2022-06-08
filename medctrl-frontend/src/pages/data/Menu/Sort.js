// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import VariableSelect from '../../../shared/VariableSelect/VariableSelect'

// Returns the filter item in HTML
function displayItem(props) {
  return (
    <div id={props.id} className="med-table-menu-sort-item">
      <VariableSelect
        className="med-table-menu-select med-select"
        defaultValue={props.item.selected}
        onChange={(e) => props.sel(props.id, e.target.value)}
        dataTestId="sort-select-attr"
      />
      <select
        className="med-table-menu-select med-select"
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
        className="bx bxs-x-circle med-table-menu-delete-button med-primary-text"
        data-testid="delete-sorting-box"
        onClick={() => props.del(props.id)}
      ></i>
    </div>
  )
}

export default displayItem
