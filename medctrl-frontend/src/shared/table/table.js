import React from 'react'
import './table.css'

//Function based component, returns table
function DisplayTable({
  data,
  selectTable,
  searchTable,
  selectedTable,
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
  const allSelected = getAllSelected(checkedState)

  //Handle a mouseclick on a checkbox in the normal row
  const handleOnChange = (key) => {
    const updatedCheckedState = JSON.parse(JSON.stringify(checkedState)) //hard copy state
    updatedCheckedState[key] = !updatedCheckedState[key]
    setCheckedState(updatedCheckedState)
  }

  //Handle a mouseclick on the checkbox in the header
  const handleAllChange = () => {
    const updatedCheckedState = JSON.parse(JSON.stringify(checkedState)) //hard copy state
    data.forEach((prop) => {
      updatedCheckedState[prop.EUNumber] = !allSelected
    })
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
              value={checkedState[entry.EUNumber]}
              onChange={handleOnChange.bind(null, entry.EUNumber)}
              data={data}
            />
          ) : null}
          {Object.values(entry).map((propt, index2) => {
            return (
              <td className="med_td" key={index2}>
                {propt}
              </td>
            )
          })}
          <InfoboxColumn />
          {!selectTable && !searchTable && (
            <BinboxColumn onp={handleOnChange.bind(null, entry.EUNumber)} />
          )}
        </tr>
      )
    })

  //return table, with a header with the data keywords
  return (
    <table className="med_table">
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
                return (
                  <th className="med_th" key={index}>
                    {key}
                  </th>
                )
              })
          }
          {
            //if selectedTable, add coloredbar to the header
            <td className="med_td smallColumn"></td>
          }
          {
            //if selectedTable, add coloredbar to the header
            selectedTable ? <td className="med_td smallColumn"></td> : null
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
    <td className="med_td smallColumn">
      <input
        className="tableCheckboxColumn"
        type="checkbox"
        checked={value}
        onChange={onChange}
      />
    </td>
  )
}

//logic for the bin
function BinboxColumn({ onp }) {
  return (
    <td className="med_td smallColumn">
      <i className="bx bx-trash icons" onClick={onp}></i>
    </td>
  )
}

//logic for the information button
function InfoboxColumn() {
  return (
    <td className="med_td smallColumn">
      <i className="bx bx-info-circle icons" />
    </td>
  )
}

function getAllSelected(checkedState) {
  let allBoolean = true
  for (const prop in checkedState) {
    allBoolean = allBoolean && checkedState[prop]
  }
  return allBoolean
}
export default DisplayTable
