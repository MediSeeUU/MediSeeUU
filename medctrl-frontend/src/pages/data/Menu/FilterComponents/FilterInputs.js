import React from 'react'

function FilterInputs(container) {
  switch (container.props.item.filterType) {
    case 'text':
      return textFilter(container)
    case 'number':
      return numFilter(
        container,
        container.props.item.input[container.i].filterRange
      )
    case 'date':
      return dateFilter(
        container,
        container.props.item.input[container.i].filterRange
      )
    case 'bool':
      return BoolFilter(container)
    default:
      throw Error('filter type invalid')
  }
}

function textFilter(container) {
  return (
    <input
      type="text"
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

function numFilter(container, filterRange) {
  if (filterRange === 'from') {
    return (
      <input
        type="number"
        id={container.i + container.props.item.selected + 'from'}
        className="med-table-menu-filter-input-field med-num-input"
        defaultValue={container.props.item.input[container.i].var}
        placeholder="Enter value"
        onBlur={(e) =>
          container.props.fil(container.props.id, container.i, e.target.value)
        }
        data-testid="filter-input-num-from"
      />
    )
  } else if (filterRange === 'till') {
    return (
      <input
        type="number"
        id={container.i + container.props.item.selected + 'till'}
        className="med-table-menu-filter-input-field med-num-input"
        defaultValue={container.props.item.input[container.i].var}
        placeholder="Enter value"
        onBlur={(e) =>
          container.props.fil(container.props.id, container.i, e.target.value)
        }
      />
    )
  } else {
    console.error('Invalid filter range in FilterInputs')
    return null
  }
}

function dateFilter(container, filterRange) {
  if (filterRange === 'from') {
    return (
      <input
        type="date"
        id={container.i + container.props.item.selected + 'from'}
        className="med-table-menu-filter-input-field med-date-input"
        defaultValue={container.props.item.input[container.i].var}
        placeholder="Enter value"
        onBlur={(e) =>
          container.props.fil(container.props.id, container.i, e.target.value)
        }
      />
    )
  } else if (filterRange === 'till') {
    return (
      <input
        type="date"
        id={container.i + container.props.item.selected + 'till'}
        className="med-table-menu-filter-input-field med-date-input"
        defaultValue={container.props.item.input[container.i].var}
        placeholder="Enter value"
        onBlur={(e) =>
          container.props.fil(container.props.id, container.i, e.target.value)
        }
      />
    )
  } else {
    console.error('Invalid filter range in FilterInputs')
    return null
  }
}

function BoolFilter(container) {
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
