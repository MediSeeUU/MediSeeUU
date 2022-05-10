import React, { useState} from 'react'

function FilterInputs(container) {
  const [filterType, setFilterType] = useState('range')
  
  // TODO: make determineFilterType conditional on the data type
  return (
    <>
    {
      (container.type === 'number' || container.type === 'date') &&
      determineFilterType(setFilterType)
    }
    {constructHtml(container, filterType)}
    </>
  )

}


function determineFilterType(setFilterType) {
  return (
    <select className='filter-type' onChange={(e) => setFilterType(e.target.value)}>
      <option value='range'>Range</option>
      <option value='from'>From</option>
      <option value='till'>Till</option>
    </select>
  )
}

function constructHtml(container, filterType) {
switch (container.type) {
  case 'text':
    return textFilter(container);
  case 'number':
    return numFilter(container, filterType)
  case 'date':
    return dateFilter(container, filterType)
  case 'bool':
    return boolFilter(container)
  case 'option':
    return optionFilter(container)
  default:
    console.error("filter type invalid")
    break;
}}

function textFilter(container) {
  return  (
    <input
    type="text"
    id={container.i}
    className="filter-input med-text-input"
    defaultValue={container.props.item.input[container.i]}
    placeholder="Enter value"
    onBlur={(e) => container.props.fil(container.props.id, container.i, e.target.value)}
    data-testid="filter-input"
  />
  )}

function numFilter(container, filterType) {
  console.log(container)
  return (
    <>
    {(filterType === 'range' || filterType === 'from') &&
      <div>
        From:
        <input
        type="number"
        id={container.i}
        className="filter-input med-num-input"
        defaultValue={container.props.item.input[container.i]}
        placeholder="Enter value"
        onBlur={(e) => container.props.fil(container.props.id, container.i, e.target.value)}
        data-testid="filter-input"
        />
      </div>
    }

    {(filterType === 'range' || filterType === 'till') &&
      <div>
        Till:
        <input
        type="number"
        id={container.i}
        className="filter-input med-num-input"
        defaultValue={container.props.item.input[container.i]}
        placeholder="Enter value"
        onBlur={(e) => container.props.fil(container.props.id, container.i, e.target.value)}
        data-testid="filter-input"
        />
      </div>
    }
    </>
  )
}

function dateFilter() {

}

function optionFilter() {

}

function boolFilter() {

}

export default FilterInputs