import { v4 as uuidv4 } from 'uuid'
import { useStructure } from '../../../../../shared/Context/StructureContext'
import VariableSelect from '../../../../../shared/VariableSelect'
import FilterInputs from './FilterComponents/FilterInputs'

// Function based component that renders a filter item
function Filter(props) {
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
      {filterInputs(props)}
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

// Function that returns all filter input boxes
function filterInputs(props) {
  const fields = []
  for (let i = 0; i < props.item.input.length; i++) {
    fields.push(
      <div key={uuidv4()} className="filter-picker">
        {PickFilter(props, i)}
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

function PickFilter(props, i) {
  var dataType = GetDataType(props.item.selected)

  //TODO: determine the best place to catch any illegal datatypes
  const possibleTypes = ['number', 'string', 'date', 'bool']

  // If data type exists, make filter of correct type. Otherwise use text filter.
  props.item.filterType = possibleTypes.includes(dataType) ? dataType : 'string'

  // NOTE: if datatype 'string' is called 'text', it can be passed directly to abstract filter function??

  return (
    <>
      {/* If number or date, first determine filter range */}
      {(dataType === 'number' || dataType === 'date') && (
        <DetermineFilterRange container={props} i={i} />
      )}
      <FilterInputs props={props} i={i} />
    </>
  )
}

function DetermineFilterRange(props) {
  return (
    <select
      className="filter-range"
      onChange={(e) => {
        props.container.item.input[props.i].filterRange = e.target.value
        props.container.sel(props.container.id, props.container.item.selected)
      }}
      defaultValue={props.container.item.input[props.i].filterRange}
    >
      <option value="from">From</option>
      <option value="till">Till</option>
    </select>
  )
}

// Function that returns the data type of a variable
function GetDataType(selected) {
  let structData = useStructure()

  // Iterate over the categories and array entries to find the selected variable
  for (let category in structData) {
    for (var i = 0; i < structData[category].length; i++) {
      if (structData[category][i]['data-front-key'] === selected) {
        return structData[category][i]['data-format']
      }
    }
  }
}

export default Filter
