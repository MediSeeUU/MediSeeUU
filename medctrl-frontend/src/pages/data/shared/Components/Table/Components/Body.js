import React from 'react'
import {
  useCheckedState,
  useCheckedStateUpdate,
  useColumnSelection,
} from '../../../../../../shared/contexts/DataContext'
import CheckboxColumn from './CheckboxColumn'
import RightStickyActions from './RightStickyActions'
import { dataToDisplayFormat } from '../format'

// Function based component that renders the body of the table
function Body({data, select, amountPerPage, currentPage}) {
  const checkedState = useCheckedState()
  const setCheckedState = useCheckedStateUpdate()

  const columnSelection = useColumnSelection()

  // Handle a mouseclick on a checkbox in the normal row
  const handleOnChange = (key) => {
    const updatedCheckedState = JSON.parse(JSON.stringify(checkedState))
    updatedCheckedState[key] = !updatedCheckedState[key]
    setCheckedState(updatedCheckedState)
  }

  // Lower and higherbound for pagination
  const lowerBoundDataPage = amountPerPage * (currentPage - 1)
  const higherBoundDataPage = amountPerPage * currentPage

  // Adds a row for every data entry
  const htmlData = data.slice(
    lowerBoundDataPage,
    higherBoundDataPage
  ).map((entry, index1) => {
    // For every column, add the corresponding data element (after formatting)
    const body = columnSelection.map((propt, index2) => {
      return (
        <td className="med-table-body-cell" key={index2}>
          <div>{dataToDisplayFormat({ entry, propt })}</div>
        </td>
      )
    })

    // Return a row with checkbox (if select table), the data
    // and the sticky actions at the end
    return (
      <tr key={index1 + lowerBoundDataPage}>
        {select && 
          <CheckboxColumn
            value={checkedState[entry.EUNoShort]}
            onChange={handleOnChange.bind(null, entry.EUNoShort)}
          />}
        {body}
        <RightStickyActions
          entry={entry}
          select={select}
          onChange={handleOnChange}
        />
      </tr>
    )
  })

  return (
    <tbody className="med-table-body">{htmlData}</tbody>
  )
}

export default Body
