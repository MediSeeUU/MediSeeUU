// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'

// Function based component returning the specific filter input box
function FilterInputs(container) {
  switch (container.props.item.filterType) {
    case 'bool':
      return BoolFilter(container)
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
      onBlur={(e) =>
        container.props.fil(container.props.id, container.i, e.target.value)
      }
      data-testid="filter-input-text"
    />
  )
}

// Function based component that returns the input box for boolean inputs
function BoolFilter(container) {
  if (container.props.item.input[container.i].var !== 'no')
    container.props.item.input[container.i].var = 'yes'
  return (
    <select
      id={container.i + container.props.item.selected}
      className="med-table-menu-filter-input-field med-text-input"
      defaultValue={container.props.item.input[container.i].var}
      onBlur={(e) =>
        container.props.fil(container.props.id, container.i, e.target.value)
      }
      data-testid="filter-input-bool"
    >
      <option value="yes">True</option>
      <option value="no">False</option>
    </select>
  )
}

export default FilterInputs
