// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import { v4 as uuidv4 } from 'uuid'
import { useStructure } from '../../../../../shared/contexts/StructureContext'
import VariableSelect from '../../../../../shared/VariableSelect'
import FilterInputs from './FilterInputs'

// Function based component that renders a filter item
function Filter(props) {
  return (
    <div id={props.id} className="med-table-menu-filter-item">
      {/* Render the variable select */}
      <VariableSelect
        className="med-table-menu-select med-select"
        defaultValue={props.item.selected}
        onChange={(e) => props.sel(props.id, e.target.value)}
        dataTestId="filter-select"
      />
      {/* Render delete icon on the top-right */}
      <i
        className="bx bxs-x-circle med-table-menu-delete-button med-primary-text"
        onClick={() => props.del(props.id)}
        data-testid="delete-icon"
      ></i>
      {/* Render all the filter inputs */ filterInputs(props)}
      {/* Render an add label to add more filter inputs */}
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

// Function that returns all filter input boxes
function filterInputs(props) {
  const fields = []
  // Iterate over de inputs
  for (let i = 0; i < props.item.input.length; i++) {
    // Add an input box and its delete icon
    fields.push(PickFilter(props, i))
  }
  return fields
}

// Function based component that returns the specific filter inputs based on the variable type
function PickFilter(props, i) {
  // First get the datatype of the selected variable
  const dataType = GetDataType(props.item.selected)

  // Define the legal types
  const possibleTypes = ['number', 'string', 'date', 'bool']

  // The filter type is equal to the type of the variable (if not an illegal type, then we just use string)
  props.item.filterType = possibleTypes.includes(dataType) ? dataType : 'string'

  return (
    <div key={uuidv4()}>
      {/* If number or date, first determine filter range */}
      {(dataType === 'number' || dataType === 'date') && (
        <DetermineFilterRange container={props} i={i} />
      )}
      {/* Render input box */}
      <FilterInputs props={props} i={i} />
      {/* Render remove icon to remove the input box */}
      <i
        className="bx bxs-minus-circle med-table-menu-remove-filter-option-icon"
        onClick={() => props.dbox(props.id, i)}
        data-testid="remove-icon"
      ></i>
    </div>
  )
}

// Function that returns the a filter range select
// The options are: 'From' and 'Till'
function DetermineFilterRange(props) {
  return (
    <select
      className="med-table-menu-filter-input-field med-text-input"
      onChange={(e) => {
        props.container.item.input[props.i].filterRange = e.target.value
        props.container.sel(props.container.id, props.container.item.selected)
      }}
      defaultValue={props.container.item.input[props.i].filterRange}
    >
      <option value="from">From</option>
      <option value="till">Till</option>
    </select>
  )
}

// Function that returns the data type of a variable
function GetDataType(selected) {
  const structData = useStructure()

  // Iterate over the categories and array entries to find the selected variable
  // Then return the type of that variable
  for (let category in structData) {
    for (var i = 0; i < structData[category].length; i++) {
      if (structData[category][i]['data-front-key'] === selected) {
        return structData[category][i]['data-format']
      }
    }
  }
}

export default Filter
