import { v4 as uuidv4 } from 'uuid'
import VariableSelect from '../../../shared/VariableSelect/VariableSelect'
import FilterInputs from './FilterComponents/FilterInputs'
import { StructureContext } from '../../../shared/contexts/DataContext'
import structData from '../../../shared/contexts/structServer.json'

// Returns all filter input boxes in HTML
function filtersToHTML(props) {
  const fields = []
  for (let i = 0; i < props.item.input.length; i++) {
    fields.push(
      <div key={uuidv4()} className="filter-picker">

        {
        pickFilter(props, i)
        }
        <i
          className="bx bxs-minus-circle med-table-menu-remove-filter-option-icon"
          onClick={() => props.dbox(props.id, i)}
          data-testid="remove-icon"
        ></i>
      </div>
    )
  }
  return fields
}

// Returns the filter item in HTML
function DisplayItem(props) {
  return (
    <div id={props.id} className="med-table-menu-filter-item">
      <VariableSelect
        className="med-table-menu-select med-select"
        defaultValue={props.item.selected}
        onChange={(e) => props.sel(props.id, e.target.value)}
        dataTestId="filter-select"
      />
      <i
        className="bx bxs-x-circle med-table-menu-delete-button med-primary-text"
        onClick={() => props.del(props.id)}
        data-testid="delete-icon"
      ></i>
      {filtersToHTML(props)}
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

function pickFilter(props, i) {

  // console.log(structData['General Information'][0]['data-front-key'])
  var dataType = GetDataType(props.item.selected)
  console.log(dataType)

  // if (textVars.includes(props.item.selected) || tempTextVars.includes(props.item.selected)) {
  if (dataType === 'string') {
    props.item.filterType = 'text'
    return (<FilterInputs 
      props = {props}
      i = {i} 
    />
  )}

  // else if (numVars.includes(props.item.selected) || tempNumVars.includes(props.item.selected)) {
  else if (dataType === 'number') {
    props.item.filterType = 'number'

    return (
      <>
        <DetermineFilterRange 
        container = {props}
        i = {i} 
        />
        <FilterInputs 
          props = {props}
          i = {i}
        />
      </>
  )}

  // else if (dateVars.includes(props.item.selected) || tempDateVars.includes(props.item.selected)){
  else if (dataType === 'date') {
    props.item.filterType = 'date'

    return (
      <>
        <DetermineFilterRange 
        container = {props}
        i = {i} 
        />
        <FilterInputs 
          props = {props}
          i = {i}
        />
      </>
  )}

  // else if (boolVars.includes(props.item.selected) || tempBoolVars.includes(props.item.selected)){
  else if (dataType === 'bool') {
    props.item.filterType = 'bool'
    return (
      <FilterInputs 
        props = {props}
        i = {i}
      />
  )}

  else {
    console.log("No valid data type, continuing as text filter")
    props.item.filterType = 'text'
    return (
      <FilterInputs 
        props = {props}
        i = {i}
      />
  )}
}

function DetermineFilterRange(props) {
  return (
    <select 
      className='filter-range' 
      onChange={(e) => {
        props.container.item.input[props.i].filterRange = e.target.value
        props.container.sel(props.container.id, props.container.item.selected) // Force component rerender
      }}
      defaultValue={props.container.item.input[props.i].filterRange}
      >
      {/* <option value='range'>Range</option> */}
      <option value='from'>From</option>
      <option value='till'>Till</option>
    </select>
  )
}

function GetDataType(selected) {
  //Loop over all categories and array entries to find the selected variable
  for (let category in structData) {
    for (var i=0; i < structData[category].length; i++) {
      if (structData[category][i]['data-front-key'] === selected) {
        return structData[category][i]['data-format']
      }
    }
  }
}

export default DisplayItem
