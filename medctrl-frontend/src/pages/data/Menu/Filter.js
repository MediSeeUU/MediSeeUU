import { v4 as uuidv4 } from 'uuid'
import FilterInputs from './FilterComponents/FilterInputs'

// Returns all filter input boxes in HTML
function filtersToHTML(props) {
  const fields = []
  for (let i = 0; i < props.item.input.length; i++) {
    fields.push(
      <div key={uuidv4()} className="filter-picker">
        {pickFilter(props, i)}
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
      <select
        className="med-table-menu-select med-select"
        defaultValue={props.item.selected}
        onChange={(e) => props.sel(props.id, e.target.value)}
        data-testid="filter-select"
      >
        <option key="" value="" hidden>
          Select a variable...
        </option>
        {props.options}
      </select>
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

// variable type hardcoded for now. eventually change later if time/convenient :)

// TODO: check for changes in var name between versions

// these lists are from the endpoints, second set of lists from the JSON data file for testing.
// second set of lists can be removed once data is retrieved from DB instead
// TODO: double check all these names once context is filled from DB instead of test JSON
const textVars = ['newactivesubstance', 'emaurl', 'ecurl', 'atccode', 'activesubstance', 
  'medicinetype', 'decisionurl', 'annexurl', 'eparurl', 'rapporteur', 'corapporteur', 'brandname']

const numVars = ['eunumber', 'emanumber', 'authorisationtotaltime', 'authorisationactivetime',
 'authorisationstoppedtime', 'decisiontime']

const dateVars = ['decisiondate']

const boolVars = ['atmp', 'referral', 'suspension', 'acceleratedgranted',
  'acceleratedmaintained', 'prime', 'orphan']

const optionVars = ['legalbasis', 'legalscope', 'status']


// SECOND SET OF LISTS TO WORK WITH THE DATA FROM JSON TEST FILE
const tempTextVars = [ 'EUNumber', 'ATCNameL2', 'ATCCodeL2', 'Rapporteur', 'CoRapporteur',
 'BrandName', 'MAH', 'ActiveSubstance', 'Period', 'ATCCodeL1', 'LegalSCope', 'LegalType', 'PRIME']

const tempNumVars = ['TotalTimeElapsed', 'ClockStopElapsed', 'ActiveTimeElapsed',
 'EUNoShort', 'DecisionYear', 'ApplicationNo']

const tempDateVars = ['DecisionDate']

const tempBoolVars = ['ATMP', 'AcceleratedExecuted', 'AcceleratedGranted', 'NAS',
 'OrphanDesignation', 'NASQualified', 'CMA', 'AEC', 'PRIME']

const tempOptionVars = []

// end of variable hardcoding

function pickFilter(props, i) {
  if (textVars.includes(props.item.selected) || tempTextVars.includes(props.item.selected)) {
    props.item.filterType = 'text'
    return (<FilterInputs 
      props = {props}
      i = {i} 
    />
  )}

  else if (numVars.includes(props.item.selected) || tempNumVars.includes(props.item.selected)) {
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

  else if (dateVars.includes(props.item.selected) || tempDateVars.includes(props.item.selected)){
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

  else if (boolVars.includes(props.item.selected) || tempBoolVars.includes(props.item.selected)){
    props.item.filterType = 'bool'
    return (
      <FilterInputs 
        props = {props}
        i = {i}
      />
  )}

  else if (optionVars.includes(props.item.selected) || tempOptionVars.includes(props.item.selected)){
    props.item.filterType = 'option'
    return (
      <FilterInputs 
        props = {props}
        i = {i}
      />
  )}

  else {
    console.error("Variable doesn't have a filter type set, continuing as text filter")
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


export default DisplayItem
