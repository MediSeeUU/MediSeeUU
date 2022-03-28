import React, { useState } from 'react'
import './table.css'

//Function based component, returns table
function DisplayTable({
  data,
  selectTable,
  amountPerPage,
  currentPage,
  checkedState,
  setCheckedState,
}) {
  //throw error if parameters not defined
  if (!data || !amountPerPage || !currentPage) {
    throw Error('parameters data, amountPerPage and currentPage are mandatory')
  }
  //throw error when table is a select table but selected data is not handled
  if (selectTable && (!setCheckedState || !checkedState)) {
    throw Error('If table is a select table, dataToParent should be defined')
  }

  //Check if all checkboxes are checked, used to check/uncheck the checkbox in the header
  const allSelected =
    checkedState?.find((item) => {
      return !item
    }) ?? true

  //Handle a mouseclick on a checkbox in the normal row
  const handleOnChange = (position) => {
    const updatedCheckedState = checkedState.map((item, index) =>
      index === position ? !item : item
    )
    setCheckedState(updatedCheckedState)
  }

  //Handle a mouseclick on the checkbox in the header
  const handleAllChange = () => {
    const updatedCheckedState = new Array(data.length).fill(!allSelected)
    setCheckedState(updatedCheckedState)
  }

  //lower and higherbound for pagination
  const lowerBoundDataPage = amountPerPage * (currentPage - 1)
  const higherBoundDataPage = amountPerPage * currentPage

  if (lowerBoundDataPage > data.length) {
    throw Error('Pagination too high, data not defined')
  }

  //constant with the table body data, for every data entry add a new row
  const htmlData = data
    .slice(lowerBoundDataPage, higherBoundDataPage)
    .map((entry, index1) => {
      return (
        <tr key={index1 + lowerBoundDataPage}>
          {selectTable ? (
            <CheckboxColumn
              value={checkedState[index1 + lowerBoundDataPage]}
              onChange={handleOnChange.bind(null, index1 + lowerBoundDataPage)}
              data={data}
            />
          ) : null}
          {Object.values(entry).map((propt, index2) => {
            return <td key={index2}>{propt}</td>
          })}
        </tr>
      )
    })

  //return table, with a header with the data keywords
  return (
    <table>
      <thead className="tableHeader">
        <tr>
          {
            //if selectTable, add check all checkbox to the header
            selectTable ? (
              <CheckboxColumn
                value={allSelected}
                onChange={handleAllChange}
                data={data}
              />
            ) : null
          }
          {
            //add object keys to the table header
            data.length > 0 &&
              Object.keys(data[0]).map((key, index) => {
                return <th key={index}>{key}</th>
              })
          }
        </tr>
      </thead>
      <tbody className="tableBody">{htmlData}</tbody>
    </table>
  )
}

//logic for the checkboxes
const CheckboxColumn = ({ value, onChange }) => {
  return (
    <td className="checkboxColumn">
      <input type="checkbox" checked={value} onChange={onChange} />
    </td>
  )
}

export default DisplayTable
