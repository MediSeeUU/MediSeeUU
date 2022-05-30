import React from 'react'

function FilterInputs(container) {
  // TODO: if datatype string can be switched to text, this statement can be removed
  if (container.props.item.filterType === 'string')
    container.props.item.filterType = 'text'

  switch (container.props.item.filterType) {
    case 'text':
      return inputFilter(
        container,
        container.props.item.input[container.i].filterRange
      )
    case 'number':
      return inputFilter(
        container,
        container.props.item.input[container.i].filterRange
      )
    case 'date':
      return inputFilter(
        container,
        container.props.item.input[container.i].filterRange
      )
    case 'bool':
      return boolFilter(container)
    default:
      throw Error('filter type invalid')
  }
}

function inputFilter(container, filterRange) {
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

function boolFilter(container) {
  if (container.props.item.input[container.i].var !== 'no')
    container.props.item.input[container.i].var = 'yes'
  return (
    <div>
      <select
        id={container.i + container.props.item.selected}
        className="med-table-menu-filter-input-field med-bool-input"
        defaultValue={container.props.item.input[container.i].var}
        onBlur={(e) =>
          container.props.fil(container.props.id, container.i, e.target.value)
        }
        data-testid="filter-input-bool"
      >
        <option value="yes">True</option>
        <option value="no">False</option>
      </select>
    </div>
  )
}

export default FilterInputs
