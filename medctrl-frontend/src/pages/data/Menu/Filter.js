import { v4 as uuidv4 } from 'uuid'
import FilterInputs from './FilterComponents/FilterInputs'

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
          className="bx bxs-minus-circle remove-icon"
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
    <div id={props.id} className="filter-item">
      <select
        className="select med-select"
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
        className="bx bxs-x-circle delete med-primary-text"
        onClick={() => props.del(props.id)}
        data-testid="delete-icon"
      ></i>
      {filtersToHTML(props)}
      <label
        className="add-label med-primary-text"
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
const tempTextVars = ['ATCNameL2', 'ATCCodeL2', 'Rapporteur', 'CoRapporteur',
 'BrandName', 'MAH', 'ActiveSubstance' ]

const tempNumVars = ['EUNumber', 'TotalTimeElapsed', 'ClockStopElapsed', 'ActiveTimeElapsed',
 'EUNoShort', 'DecisionYear', 'ApplicationNo']

const tempDateVars = ['DecisionDate']

const tempBoolVars = ['ATMP', 'AcceleratedExecuted', 'AcceleratedGranted', 'NAS',
 'OrphanDesignation', 'NASQualified', 'CMA', 'AEC']

const tempOptionVars = ['Period', 'ATCCodeL1', 'LegalSCope', 'LegalType', 'PRIME']

// end of variable hardcoding

function pickFilter(props, i) {
  if (textVars.includes(props.item.selected) || tempTextVars.includes(props.item.selected)) {
    console.log("text type entered")
    return (<FilterInputs 
      type = {"text"}
      props = {props}
      i = {i} 
    />
  )}

  else if (numVars.includes(props.item.selected) || tempNumVars.includes(props.item.selected)) {
    console.log("number type entered")
    return (
      <FilterInputs 
        type = {"number"}
        props = {props}
        i = {i}
      />
  )}

  else if (dateVars.includes(props.item.selected) || tempDateVars.includes(props.item.selected)){
    console.log("date type entered")
    return (
      <FilterInputs 
        type = {"date"}
        props = {props}
        i = {i}
      />
  )}

  else if (boolVars.includes(props.item.selected) || tempBoolVars.includes(props.item.selected)){
    console.log("bool type entered")
    return (
      <FilterInputs 
        type = {"bool"}
        props = {props}
        i = {i}
      />
  )}

  else if (optionVars.includes(props.item.selected) || tempOptionVars.includes(props.item.selected)){
    console.log("option type entered")
    return (
      <FilterInputs 
        type = {"option"}
        props = {props}
        i = {i}
      />
  )}

  else {
    console.error("Variable doesn't have a filter type, continuing as text filter")
    return (
      <FilterInputs 
        type = {"text"}
        props = {props}
        i = {i}
      />
  )}
}




export default DisplayItem
