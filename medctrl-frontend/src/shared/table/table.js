import React, {useEffect, useState} from 'react'
import {
  useCheckedState,
  useCheckedStateUpdate,
  useColumnSelection,
  useColumnSelectionUpdate,
} from '../contexts/DataContext'
import './table.css'
import { Link } from 'react-router-dom'
import  sortData  from '../../pages/data/Utils/sorting.js'


//Function based component, returns table
function DisplayTable({
  data,
  selectTable,
  searchTable,
  amountPerPage,
  currentPage,
  menu,
  setSorters
}) {
  //throw error if parameters not defined
  if (!data || !amountPerPage || !currentPage) {
    throw Error('parameters data, amountPerPage and currentPage are mandatory')
  }

  const [LocalTableData, setLocalTableData] = useState(data)
  
  useEffect(() => {
    setLocalTableData(data)
  }, [data])
  
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
    LocalTableData.forEach((prop) => {
      updatedCheckedState[prop.EUNumber] = !allSelected
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
  const htmlData = LocalTableData
    .slice(lowerBoundDataPage, higherBoundDataPage)
    .map((entry, index1) => {
      return (
        <tr key={index1 + lowerBoundDataPage} className="med_rows">
          {selectTable ? (
            <CheckboxColumn
              value={checkedState[entry.EUNumber]}
              onChange={handleOnChange.bind(null, entry.EUNumber)}
              data={LocalTableData}
            />
          ) : null}
          {columnSelection.map((propt, index2) => {
            return (
                      <td className="med_td" key={index2}>
                        {dataToDisplayFormat({entry, propt})}
                      </td>
                    )
           
            
          })}
          <InfoboxColumn EUidNumber={entry.EUNoShort} />
          {!selectTable && !searchTable && (
            <BinboxColumn onp={handleOnChange.bind(null, entry.EUNumber)} />
          )}
        </tr>
      )
    })

  //return table, with a header with the data keywords
  return (
    <>
      <div className="addRmCollumn">
        <i
          className="bx-plusMinus bx bxs-plus-square med-primary-text"
          onClick={() => addColumn()}
          data-testid="add-column"
        />

        <i
          className="bx-plusMinus bx bxs-minus-square med-primary-text"
          onClick={() => removeColumn()}
          data-testid="remove-column"
        />

        {menu}
      </div>

      <table className="med_table">
        <thead className="tableHeader">
          <tr className="med_rows">
            {
              //if selectTable, add check all checkbox to the header
              selectTable ? (
                <CheckboxColumn
                  value={allSelected}
                  onChange={handleAllChange}
                  data={LocalTableData}
                />
              ) : null
            }
            {
              //add object keys to the table header
              columnSelection.map((key1, index1) => {
                return (
                  <th key={index1} className="med_th">
                    <select
                      value={key1}
                      className="med_th_select"
                      onChange={(e) =>
                        handleColumnChange(index1, e.target.value)
                      }
                    >
                      {Object.keys(LocalTableData[0]).map((key2, index2) => {
                        return (
                          <option key={index2} value={key2}>
                            {key2}
                          </option>
                        )
                      })}
                    </select>
                    
                    
                    <button
                        className="med_th_sort"
                        onClick={(e) => handleSortingChange(key1, "asc")}
                      >
                        ^
                      </button>
                      <button
                        className="med_th_sort"
                        onClick={(e) => handleSortingChange(key1, "desc")}
                      >
                        v
                      </button>
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
              !selectTable && !searchTable ? (
                <td className="med_td smallColumn"></td>
              ) : null
            }
          </tr>
        </thead>
        <tbody className="tableBody">{htmlData}</tbody>
      </table>
    </>
  )
}

//backend received data can be reformatted when displayed in the table
//depeding on the property/variable, different formatting may be applicable
export const dataToDisplayFormat = ({entry, propt})=>{
  switch(propt)
  {
    case "DecisionDate":
      return (slashDateToStringDate(entry[propt]))
    default:
      return (entry[propt])
  }
  
}
function slashDateToStringDate(date)
{
  var splitteddate = date.split('/')
  const day = splitteddate[1].replace(/^0+/, '')
  const month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][parseInt(splitteddate[0].replace(/^0+/, ''))-1]
  const year = splitteddate[2]
  const fullDate = day + ' '+ month + ' ' + year
  return fullDate
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
      <i className="bx bx-trash icons med-primary-text" onClick={onp}></i>
    </td>
  )
}

//logic for the information button
function InfoboxColumn({ EUidNumber }) {
  return (
    <td className="med_td smallColumn">
      <Link to={`/details/${EUidNumber}`}>
        <i
          className="bx bx-info-circle icons med-primary-text"
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
