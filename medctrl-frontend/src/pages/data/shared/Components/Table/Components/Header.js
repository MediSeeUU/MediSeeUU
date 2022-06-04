import React from 'react'
import VariableSelect from '../../../../../../shared/VariableSelect'
import {
  useCheckedState,
  useCheckedStateUpdate,
  useColumnSelection,
  useColumnSelectionUpdate,
} from '../../../../../../shared/contexts/DataContext'
import CheckboxColumn from './CheckboxColumn'

// Function based component that renders the header of the table
function Header({ select, sorters, setSorters }) {
  const columnSelection = useColumnSelection()
  const setColumnSelection = useColumnSelectionUpdate()

  const checkedState = useCheckedState()
  const setCheckedState = useCheckedStateUpdate()

  // Check if all checkboxes are checked, used to check/uncheck the checkbox in the header
  const allSelected = Object.values(checkedState).every((value) => value)

  // Handler that changes the column based on the target value
  const handleColumnChange = (id, value) => {
    let newColumnSelection = [...columnSelection]
    newColumnSelection[id] = value
    setColumnSelection(newColumnSelection)
  }

  // Handle sort change
  const handleSortingChange = (attribute, value) => {
    setSorters([{ selected: attribute, order: value }])
  }

  // Checks if the data on the given attribute is ordered ascendingly
  const isSorted = (attribute) => {
    return sorters.some(
      (element) => element.selected === attribute && element.order === 'asc'
    )
  }

  // Handle a mouseclick on the checkbox in the header
  const handleAllChange = () => {
    let updatedCheckedState = JSON.parse(JSON.stringify(checkedState))
    Object.keys(updatedCheckedState).forEach((key) => {
      updatedCheckedState[key] = !allSelected
    })
    setCheckedState(updatedCheckedState)
  }

  // Create the header by rendering all the columns
  const columns = columnSelection.map((key, index) => {
    return (
      <th key={index} className="med-table-header-cell">
        <VariableSelect
          className="med-table-header-select-cell"
          onChange={(e) => handleColumnChange(index, e.target.value)}
          defaultValue={key}
        />
        {!isSorted(key) ? (
          <i
            className="bx bxs-down-arrow med-table-header-sort"
            onClick={(e) => handleSortingChange(key, 'asc')}
          />
        ) : (
          <i
            className="bx bxs-up-arrow med-table-header-sort"
            onClick={(e) => handleSortingChange(key, 'desc')}
          />
        )}
      </th>
    )
  })

  return (
    <thead className="med-table-header">
      <tr className="">
        {select && (
          <CheckboxColumn value={allSelected} onChange={handleAllChange} />
        )}
        {columns}
        <td className="med-table-body-cell med-table-narrow-column med-column-right"></td>
      </tr>
    </thead>
  )
}

export default Header
