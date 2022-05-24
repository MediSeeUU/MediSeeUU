import React, { useEffect, useState } from 'react'
import {
  useCheckedState,
  useCheckedStateUpdate,
  useColumnSelection,
  useColumnSelectionUpdate,
} from '../contexts/DataContext'
import './table.css'
import { Link } from 'react-router-dom'
import '../../core/login/connectionServer'
import VariableSelect from '../VariableSelect/VariableSelect'

//Function based component, returns table
function DisplayTable({
  data,
  selectTable,
  searchTable,
  amountPerPage,
  currentPage,
  baseMenu,
  saveMenu,
  setSorters,
}) {
  //throw error if parameters not defined
  if (!data || !amountPerPage || !currentPage) {
    throw Error('parameters data, amountPerPage and currentPage are mandatory')
  }

  const [LocalTableData, setLocalTableData] = useState(data)

  useEffect(() => {
    setLocalTableData(data)
  }, [data])

  let token = sessionStorage.getItem('token')
  let loggedin = token != null

  const checkedState = useCheckedState()
  const setCheckedState = useCheckedStateUpdate()

  //column selection methods
  const columnSelection = useColumnSelection()
  const setColumnSelection = useColumnSelectionUpdate()

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
      updatedCheckedState[prop.EUNoShort] = !allSelected
    })
    setCheckedState(updatedCheckedState)
  }

  //lower and higherbound for pagination
  const lowerBoundDataPage = amountPerPage * (currentPage - 1)
  const higherBoundDataPage = amountPerPage * currentPage

  if (lowerBoundDataPage > LocalTableData.length) {
    throw Error('Pagination too high, data not defined')
  }

  //handler that changes the column based on the target value
  const handleColumnChange = (id, value) => {
    let newColumnSelection = [...columnSelection]
    newColumnSelection[id] = value
    setColumnSelection(newColumnSelection)
  }

  //handler that changes the data sorting order
  const handleSortingChange = (attributename, value) => {
    setSorters([{ selected: attributename, order: value }])
  }

  //handler that adds a column
  const addColumn = () => {
    let allColumnOptions = Object.keys(LocalTableData[0])
    let availableColumns = allColumnOptions.filter(
      (element) => ![...columnSelection].includes(element)
    )

    if (availableColumns.length > 0) {
      let newColumnName = availableColumns[0]
      let newColumnSelection = [...columnSelection]
      newColumnSelection.push(newColumnName)
      setColumnSelection(newColumnSelection)
    }
  }

  //handler that removes a column
  const removeColumn = () => {
    if (columnSelection.length > 5) {
      let newColumnSelection = [...columnSelection]
      newColumnSelection.pop()
      setColumnSelection(newColumnSelection)
    }
  }

  //constant with the table body data, for every data entry add a new row
  const htmlData = LocalTableData.slice(
    lowerBoundDataPage,
    higherBoundDataPage
  ).map((entry, index1) => {
    return (
      <tr key={index1 + lowerBoundDataPage} className="med_rows">
        {selectTable ? (
          <CheckboxColumn
            value={checkedState[entry.EUNoShort]}
            onChange={handleOnChange.bind(null, entry.EUNoShort)}
            data={LocalTableData}
          />
        ) : null}
        {columnSelection.map((propt, index2) => {
          return (
            <td className="med-table-body-cell" key={index2}>
              <div>{dataToDisplayFormat({ entry, propt })}</div>
            </td>
          )
        })}
        <RightStickyActions
          EUidNumber={entry.EUNoShort}
          selectTable={selectTable}
          searchTable={searchTable}
          entry={entry}
          handleOnChange={handleOnChange}
        />
      </tr>
    )
  })

  //return table, with a header with the data keywords
  return (
    <>
      <div className="med-add-remove-button-container">
        <i
          className="med-add-remove-button bx bxs-plus-square med-primary-text"
          onClick={() => addColumn()}
          data-testid="add-column"
        />
        <i
          className="med-add-remove-button bx bxs-minus-square med-primary-text"
          onClick={() => removeColumn()}
          data-testid="remove-column"
        />

        {baseMenu}
        {loggedin && saveMenu}
      </div>

      <table className="med-table">
        <thead className="med-table-header">
          <tr className="">
            {
              //if selectTable, add check all checkbox to the header
              selectTable && (
                <CheckboxColumn
                  value={allSelected}
                  onChange={handleAllChange}
                  data={LocalTableData}
                />
              )
            }
            {
              //add object keys to the table header
              columnSelection.map((key1, index1) => {
                return (
                  <th key={index1} className="med-table-header-cell">
                    <VariableSelect
                      className="med-table-header-select-cell"
                      onChange={(e) =>
                        handleColumnChange(index1, e.target.value)
                      }
                      defaultValue={key1}
                    />

                    <button
                      className="med_th_sort"
                      onClick={(e) => handleSortingChange(key1, 'asc')}
                    >
                      ^
                    </button>

                    <button
                      className="med_th_sort"
                      onClick={(e) => handleSortingChange(key1, 'desc')}
                    >
                      v
                    </button>
                  </th>
                )
              })
            }
            {
              //if selectedTable, add coloredbar to the header
              <td className="med-table-body-cell med-table-narrow-column med-column-right"></td>
            }
          </tr>
        </thead>
        <tbody className="med-table-body">{htmlData}</tbody>
      </table>
    </>
  )
}

//backend received data can be reformatted when displayed in the table
//depeding on the property/variable, different formatting may be applicable
export const dataToDisplayFormat = ({ entry, propt }) => {
  switch (propt) {
    case 'DecisionDate':
      return slashDateToStringDate(entry[propt])
    default:
      return entry[propt]
  }
}
function slashDateToStringDate(date) {
  const defValue = 'NA'
  if (date === defValue) {
    return date
  }
  var splitteddate = date.split('/')
  const day = splitteddate[1].replace(/^0+/, '')
  const month = [
    'Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec',
  ][parseInt(splitteddate[0].replace(/^0+/, '')) - 1]
  const year = splitteddate[2]
  const fullDate = day + ' ' + month + ' ' + year
  return fullDate
}

//logic for the checkboxes
const CheckboxColumn = ({ value, onChange }) => {
  return (
    <td className="med-table-body-cell med-table-narrow-column med-column-left">
      <input
        className="tableCheckboxColumn"
        type="checkbox"
        checked={!value ? false : value}
        onChange={onChange}
      />
    </td>
  )
}

//Component that holds actions that are always on the right of the table
function RightStickyActions({
  EUidNumber,
  selectTable,
  searchTable,
  entry,
  handleOnChange,
}) {
  return (
    <td className="med-table-body-cell med-table-narrow-column med-column-right">
      {/* Trash can icon, only visible on certain tables */}
      {!selectTable && !searchTable && (
        <i
          className="bx bx-trash med-table-icons med-primary-text"
          onClick={handleOnChange.bind(null, entry.EUNoShort)}
        ></i>
      )}

      {/* Link to details page */}
      <Link to={`/details/${EUidNumber}`}>
        <i
          className="bx bx-info-circle med-table-icons med-primary-text"
          id={'detailInfo' + EUidNumber}
          testid={'detailInfo' + EUidNumber}
        />
      </Link>
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
