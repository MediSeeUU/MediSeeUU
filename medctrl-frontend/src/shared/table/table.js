import React, { useState } from 'react';
import './table.css';

//Function based component, returns table
function DisplayTable({data, selectTable, dataToParent}) {
  //State variable for the selection checkboxes, for more about states see: https://reactjs.org/docs/hooks-state.html
  const [checkedState, setCheckedState] = useState(
    new Array(data.length).fill(false)
  );
  
  //Check if all checkboxes are checked, used to check/uncheck the checkbox in the header
  const allSelected = checkedState.find((item) => {
    return !item;
  }) ?? true;
  
  //Handle a mouseclick on a checkbox in the normal row
  const handleOnChange = (position) => {
    const updatedCheckedState = checkedState.map((item, index) =>
      index === position ? !item : item
    );
    setCheckedState(updatedCheckedState);
  }

  //Handle a mouseclick on the checkbox in the header
  const handleAllChange = () => {
    const updatedCheckedState = new Array(data.length).fill(!allSelected);
    setCheckedState(updatedCheckedState);
  }

  //Handle the selected data list on checkbox change, send the data to the parent
  const handleSelectedData = () => {
    const selectedData = data.filter((item, index) => {
      return checkedState[index];
    });
    dataToParent(selectedData);
  }

  //Run handleSelectedData when it is a select table and dataToParent is defined
  //This function is run on every reload, when state is set, page will 'reload'
  if (selectTable && !!dataToParent) {
    handleSelectedData();
  } else if (selectTable && !dataToParent) {
    //throw error when table is a select table but selected data is not handled
    throw Error("If table is a select table, dataToParent should be defined")
  }

  //constant with the table body data, for every data entry add a new row
  const htmlData = data.map(
    (entry, index1) => {
      return(
        <tr key={index1}>
          {
            selectTable ? 
              <CheckboxColumn 
                value={checkedState[index1]} 
                onChange={handleOnChange.bind(null, index1)}
                data={data}/> 
              : null
          }
          {
            Object.values(entry).map((propt, index2) => { 
              return( <td key={index2}>{propt}</td> ) 
              })
          }
        </tr>
      )
    }
  );

  //return table, with a header with the data keywords
  return (
    <table>
      <thead className="tableHeader">
        <tr>
          {
            //if selectTable, add check all checkbox to the header
            selectTable ? 
              <CheckboxColumn 
                value={allSelected} 
                onChange={handleAllChange}
                data={data}/> 
              : null
          }
          {
            //add object keys to the table header
            data.length > 0 && Object.keys(data[0]).map((key, index) => { 
              return( <th key={index}>{key}</th> ) 
            })
          }
        </tr>
      </thead>
        <tbody className="tableBody">{htmlData}</tbody>
    </table>
  )
}

//logic for the checkboxes
const CheckboxColumn = ({value, onChange, data, setData}) => {
  return (
    <td className="checkboxColumn"> 
      <input 
        type="checkbox" 
        checked={value} 
        onChange={onChange.bind(null, value, data, setData)}/>
    </td>
  );
}

export default DisplayTable;
