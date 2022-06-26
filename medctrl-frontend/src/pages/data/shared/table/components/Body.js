// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import CheckboxColumn from './CheckboxColumn'
import RightStickyActions from './RightStickyActions'
import { dataToDisplayFormat } from '../format'
import { useCheckedState } from '../../../../../shared/contexts/CheckedContext'
import { useColumnSelection } from '../../../../../shared/contexts/ColumnSelectionContext'

// Function based component that renders the body of the table
function Body({ data, select, amountPerPage, currentPage }) {
  const { checkedState, setCheckedState } = useCheckedState()
  const { columnSelection } = useColumnSelection()

  // Handle a mouseclick on a checkbox in the row
  const handleOnChange = (key) => {
    const updatedCheckedState = JSON.parse(JSON.stringify(checkedState))
    updatedCheckedState[key] = !updatedCheckedState[key]
    setCheckedState(updatedCheckedState)
  }

  // Lower and higherbound for pagination
  const lowerBoundDataPage = amountPerPage * (currentPage - 1)
  const higherBoundDataPage = amountPerPage * currentPage

  // Adds a row for every data entry
  const htmlData = data
    .slice(lowerBoundDataPage, higherBoundDataPage)
    .map((entry, index1) => {
      // For every column, add the corresponding data value (after reformatting)
      const body = columnSelection.map((propt, index2) => {
        return (
          <td className="med-table-body-cell" key={index2}>
            <div>{dataToDisplayFormat({ entry, propt })}</div>
          </td>
        )
      })

      // Render the whole row with the checkbox (if applicable), data and actions
      return (
        <tr key={index1 + lowerBoundDataPage}>
          {
            /* Only add a checkbox if we are rendering a table with selected datapoints */
            select && (
              <CheckboxColumn
                value={checkedState[entry.EUNoShort]}
                onChange={handleOnChange.bind(null, entry.EUNoShort)}
              />
            )
          }
          {body}
          <RightStickyActions
            entry={entry}
            select={select}
            onChange={handleOnChange}
          />
        </tr>
      )
    })

  return <tbody className="med-table-body">{htmlData}</tbody>
}

export default Body
