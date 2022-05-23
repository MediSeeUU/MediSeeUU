import React from 'react'

function FilterInputs(container) {
  switch (container.props.item.filterType) {
  case 'text':
    return textFilter(container);
  case 'number':
    return numFilter(container, container.props.item.input[container.i].filterRange)
  case 'date':
    return dateFilter(container, container.props.item.input[container.i].filterRange)
  case 'bool':
    return BoolFilter(container)
  case 'option':
    return optionFilter(container)
  default:
    throw Error("filter type invalid")
}}

function textFilter(container) {
  return  (
    <input
    type="text"
    id={container.i + container.props.item.selected}
    className="filter-input med-text-input"
    defaultValue={container.props.item.input[container.i].var}
    placeholder="Enter value"
    onBlur={(e) => container.props.fil(container.props.id, container.i, e.target.value)}    
    data-testid="filter-input"
  />
  )}

function numFilter(container, filterRange) {
  if (filterRange === 'from') {
    return (
      <input
      type="number"
      id={container.i + container.props.item.selected + 'from'}
      className="filter-input med-num-input"
      defaultValue={container.props.item.input[container.i].var}
      placeholder="Enter value"
      onBlur={(e) => container.props.fil(container.props.id, container.i, e.target.value)}
      data-testid="filter-input"
      />
    )
  }
  else if (filterRange === 'till') {
    return(
      <input
      type="number"
      id={container.i + container.props.item.selected + 'till'}
      className="filter-input med-num-input"
      defaultValue={container.props.item.input[container.i].var}
      placeholder="Enter value"
      onBlur={(e) => container.props.fil(container.props.id, container.i, e.target.value)}
      data-testid="filter-input"
      />
    )
  }

  else {
    console.error('Invalid filter range in FilterInputs')
    return null
  }
  
}

function dateFilter(container, filterRange) {
return (
  <>
    { filterRange === 'from' &&
      <div>
        <input
        type="date"
        id={container.i + container.props.item.selected + 'from'}
        className="filter-input med-date-input"
        defaultValue={container.props.item.input[container.i].var}
        placeholder="Enter value"
        onBlur={(e) => container.props.fil(container.props.id, container.i, e.target.value)}        
        data-testid="filter-input"
        />
      </div>
    }

    { filterRange === 'till' &&
      <div>
        <input
        type="date"
        id={container.i  + container.props.item.selected + 'till'}
        className="filter-input med-date-input"
        defaultValue={container.props.item.input[container.i].var}
        placeholder="Enter value"
        onBlur={(e) => container.props.fil(container.props.id, container.i, e.target.value)}        
        data-testid="filter-input"
        />
      </div>
    }

    </>
)
}

function optionFilter() {

}

function BoolFilter(container) {
  if (container.props.item.input[container.i].var !== 'no') container.props.item.input[container.i].var = 'yes'
  return (
    <div>
      <select
      id={container.i  + container.props.item.selected}
      className='filter-input med-bool-input'
      defaultValue={container.props.item.input[container.i].var}
      onBlur={(e) => container.props.fil(container.props.id, container.i, e.target.value)}>
        <option value='yes'>True</option>
        <option value='no'>False</option>
      </select>
    </div>
  )
}

export default FilterInputs
