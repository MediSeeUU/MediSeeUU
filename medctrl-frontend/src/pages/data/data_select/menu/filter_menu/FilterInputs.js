// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import { v4 as uuidv4 } from 'uuid'
import sortCategoryData from '../../../../visualizations/single_visualization/utils/sortCategoryData'

// Function based component returning the specific filter input box
function FilterInputs(container) {
  switch (container.props.item.filterType) {
    case 'bool':
      return BoolFilter(container)
    case 'string':
      return StringFilter(container)
    default:
      return InputFilter(container)
  }
}

// Function based component that returns the input box for non-boolean inputs
function InputFilter(container) {
  return (
    <input
      type={container.props.item.filterType}
      id={container.i + container.props.item.selected}
      className="med-table-menu-filter-input-field med-text-input"
      defaultValue={container.props.item.input[container.i].var}
      placeholder="Enter value"
      onBlur={(e) => {
        container.props.item.input[container.i].var = e.target.value
      }}
      data-testid="filter-input-text"
    />
  )
}

// Function based component that returns the input box for non-boolean inputs
function StringFilter(container) {
  // Function that is called after selecting the option
  const updateSelected = (e) => {
    // If the target value is empty, then user wants to customize input
    if (!e.target.value) {
      container.props.item.input[container.i].custom = true
    }
    // Otherwise the user chose a specific category
    else {
      container.props.item.input[container.i].custom = false
    }
    // Update the filter state with the new value
    container.props.fil(container.props.id, container.i, e.target.value)
  }

  return (
    <>
      <select
        className="med-table-menu-filter-input-field med-text-input"
        defaultValue={container.props.item.input[container.i].var}
        onChange={updateSelected}
        data-testid="input-select"
      >
        <option value="">Custom</option>
        {/* Show all options for the selected variable */}
        {container.props.item.selected && container.props.cats && container.props.cats[container.props.item.selected] && sortCategoryData(container.props.cats[container.props.item.selected]).map((cat) => <option key={uuidv4()} value={cat}>{cat}</option>)}
      </select>
      {/* Only show the input box if the user chose custom input */}
      {container.props.item.input[container.i].custom && InputFilter(container)}
    </>
  )
}

// Function that returns the input box for boolean inputs
function BoolFilter(container) {
  if (container.props.item.input[container.i].var !== 'no')
    container.props.item.input[container.i].var = 'yes'
  return (
    <select
      id={container.i + container.props.item.selected}
      className="med-table-menu-filter-input-field med-text-input"
      defaultValue={container.props.item.input[container.i].var}
      onBlur={(e) => {
        container.props.item.input[container.i].var = e.target.value
      }}
      data-testid="filter-input-bool"
    >
      <option value="yes">True</option>
      <option value="no">False</option>
    </select>
  )
}

export default FilterInputs
