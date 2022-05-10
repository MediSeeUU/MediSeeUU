import { v4 as uuidv4 } from 'uuid'
import FilterInputs from './FilterComponents/FilterInputs'

// Returns all filter input boxes in HTML
function filtersToHTML(props) {
  const fields = []
  // console.log(props)
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

// TODO: double check names of prime, medicine authorization holder (MAH), orphan and brand name
const textVars = ['newactivesubstance', 'emaurl', 'ecurl', 'atccode', 'activesubstance', 
  'medicinetype', 'decisionurl', 'annexurl', 'eparurl', 'rapporteur', 'corapporteur', 'brandname']

const numVars = ['eunumber', 'emanumber', 'authorisationtotaltime', 'authorisationactivetime',
 'authorisationstoppedtime', 'decisiontime']

const dateVars = ['decisiondate', ]

const boolVars = ['atmp', 'referral', 'suspension', 'acceleratedgranted',
  'acceleratedmaintained', 'prime', 'orphan']

const optionVars = ['legalbasis', 'legalscope', 'status']

// end of variable hardcoding

function pickFilter(props, i) {
  console.log(props.item)
  if (props.item.selected === "ApplicationNo") {
    return (<FilterInputs 
      type = {"text"}
      props = {props}
      i = {i} 
    />
    )}

  else if (props.item.selected === "EUNumber") {
    return (
      <FilterInputs 
        type = {"number"}
        elements = {props}
        index = {i}
      />
    )}
  else {
    console.error("Variable doesn't have a filter type")
  }
}




export default DisplayItem
