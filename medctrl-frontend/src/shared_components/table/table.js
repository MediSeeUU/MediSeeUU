import React, { useState } from 'react';
import './table.css';

//function based component, returns table
function DisplayTable({data, selectTable, dataToParent}) {
  const [checkedState, setCheckedState] = useState(
    new Array(data.length).fill(false)
  );
  

  const allSelected = checkedState.find((item) => {
    return !item;
  }) ?? true;

  const handleOnChange = (position) => {
    const updatedCheckedState = checkedState.map((item, index) =>
      index === position ? !item : item
    );
    setCheckedState(updatedCheckedState);
  }

  const handleAllChange = (event) => {
    const updatedCheckedState = new Array(data.length).fill(!allSelected);
    setCheckedState(updatedCheckedState);
  }

  const handleSelectedData = () => {
    const selectedData = data.filter((item, index) => {
      return checkedState[index];
    });
    dataToParent(selectedData);
  }

  handleSelectedData();

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
  return(
    <table>
      <thead className="tableHeader">
        <tr>
          {
            selectTable ? 
              <CheckboxColumn 
                value={allSelected} 
                onChange={handleAllChange}
                data={data}/> 
              : null
          }
          {
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

//checkbox for the selection table
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