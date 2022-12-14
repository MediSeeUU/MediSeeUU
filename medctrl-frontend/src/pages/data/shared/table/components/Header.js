// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import { useCheckedState } from '../../../../../shared/contexts/CheckedContext'
import { useColumnSelection } from '../../../../../shared/contexts/ColumnSelectionContext'
import VariableSelect from '../../../../../shared/VariableSelect'
import CheckboxColumn from './CheckboxColumn'

// Function based component that renders the header of the table
function Header({ data, select, sorters, setSorters }) {
  const { columnSelection, setColumnSelection } = useColumnSelection()
  const { checkedState, setCheckedState } = useCheckedState()

  // Check if all checkboxes are checked, used to check/uncheck the checkbox in the header
  const allSelected = data.every((element) => checkedState[element.eunumber])

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
    data.forEach((element) => {
      updatedCheckedState[element.eunumber] = !allSelected
    })
    setCheckedState(updatedCheckedState)
  }

  // Create the header by rendering all the columns
  const columns = columnSelection.map((key, index) => {
    return (
      <th key={index} className="med-table-header-cell">
        {/* Render a variable options select to change the variables displayed in the table */}
        <VariableSelect
          className="med-table-header-select-cell"
          onChange={(e) => handleColumnChange(index, e.target.value)}
          defaultValue={key}
        />
        {
          /* Renders an arrow up or down based on the current applied sorters */
          !isSorted(key) ? (
            <i
              className="bx bxs-down-arrow med-table-header-sort"
              onClick={(e) => handleSortingChange(key, 'asc')}
              data-testid="sort-asc-column"
              role={'button'}
              tabIndex={'0'}
              onKeyPress={(e) => {
                if (e.key === 'Enter') handleSortingChange(key, 'asc')
              }}
            />
          ) : (
            <i
              className="bx bxs-up-arrow med-table-header-sort"
              onClick={(e) => handleSortingChange(key, 'desc')}
              data-testid="sort-desc-column"
              role={'button'}
              tabIndex={'0'}
              onKeyPress={(e) => {
                if (e.key === 'Enter') handleSortingChange(key, 'desc')
              }}
            />
          )
        }
      </th>
    )
  })

  return (
    <thead className="med-table-header">
      <tr className="">
        {
          /* Only render a checkbox if the table displays the selected datapoints */
          select && (
            <CheckboxColumn value={allSelected} onChange={handleAllChange} />
          )
        }
        {columns}
        <td className="med-table-body-cell med-table-narrow-column med-column-right"></td>
      </tr>
    </thead>
  )
}

export default Header
