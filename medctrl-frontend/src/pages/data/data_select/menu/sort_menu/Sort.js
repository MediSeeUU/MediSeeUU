// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import VariableSelect from '../../../../../shared/VariableSelect'

// Function based component which renders a sort item
function Sort(props) {
  return (
    <div id={props.id} className="med-table-menu-sort-item">
      {/* Render the variable options select */}
      <VariableSelect
        className="med-table-menu-select med-select"
        defaultValue={props.item.selected}
        onChange={(e) => props.sel(props.id, e.target.value)}
        dataTestId="sort-select-attr"
      />
      {/* Render the sorting order options select */}
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
      {/* Render the delete icon */}
      <i
        className="bx bxs-x-circle med-table-menu-delete-button med-primary-text"
        data-testid="delete-sorting-box"
        onClick={() => props.del(props.id)}
        role={'button'}
        tabIndex={'0'}
        onKeyPress={(e) => {
          if (e.key === 'Enter') props.del(props.id)
        }}
      ></i>
    </div>
  )
}

export default Sort
