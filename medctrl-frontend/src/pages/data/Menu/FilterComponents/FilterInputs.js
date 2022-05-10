import React, { useState} from 'react'

function FilterInputs(container) {
  const [filterType, setFilterType] = useState('range')
  
  // TODO: make determineFilterType conditional on the data type
  return (
    <>
    {determineFilterType(setFilterType)} 
    {constructHtml(container, filterType)}
    {console.log("blabla")}
    {console.log(container)}
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
  case "number":
    console.log("number filter")
    return numFilter(container, filterType)
  case 'text':
    console.log("text filter")
    return textFilter(container);
  default:
    console.error("filter type invalid")
    break;
}
//TODO: make conditional return statement depending on filter type

}

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

  return (
    <p>----------------------------FKJNJKAWDHW---------------------</p>
  )
 
    
}

function dateFilter() {

}

function optionsFilter() {

}

function boolFilter() {

}

export default FilterInputs



 // var htmlElement = document.createElement('div')
  // htmlElement.className = 'filter-inputs'

  // if ((filterType === 'range') || (filterType === 'from')) {
  //   console.log("range or from")
  //   htmlElement.appendChild(document.createTextNode("From:"))
  //   htmlElement.appendChild(document.createElement('br'))

  //   let input = document.createElement('input')
  //   input.type = 'number'
  //   input.id = container.i
  //   input.className = "filter-input med-num-input"
  //   input.defaultValue = container.props.item.input[container.i]
  //   input.placeholder = 'Enter value'
  //   input.onBlur = (e) => container.props.fil(container.props.id, container.i, e.target.value)
  //   input.setAttribute('data-testid', "filter-input")

  //   htmlElement.appendChild(input)
  //   console.log(htmlElement)

  // }

  // if ((filterType === 'range') || (filterType === 'till')) {
  //   console.log("range or till")
  //   htmlElement.appendChild(document.createTextNode("Till:"))
  //   htmlElement.appendChild(document.createElement('br'))

  //   let input = document.createElement('input')
  //   input.type = 'number'
  //   input.id = container.i
  //   input.className = "filter-input med-num-input"
  //   input.defaultValue = container.props.item.input[container.i]
  //   input.placeholder = 'Enter value'
  //   input.onBlur = (e) => container.props.fil(container.props.id, container.i, e.target.value)
  //   input.setAttribute('data-testid', "filter-input")

    
  //   htmlElement.appendChild(input)
  //   console.log(htmlElement)
  // }

  // const mainFilterDiv = document.getElementsByClassName("filter-item")[0]
  // mainFilterDiv.appendChild(htmlElement)