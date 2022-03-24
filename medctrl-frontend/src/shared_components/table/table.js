import React, { useState } from 'react';
import './table.css';



//function based component, returns table
function DisplayTable({initData, selectTable}) {
  const [tdata, setData] = React.useState([]);
  //var test = data.length <= 0 //?? setData(initData)
  const data = initData;
  //constant with the table body data, for every data entry add a new row
  const htmlData = data.map(
    (entry, index1) => {
      return(
        <tr key={index1}>
          {
            selectTable ? 
              <CheckboxColumn 
                dataEntry={entry} 
                onChange={checkboxChange}
                data={null}/> 
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
  
  let selectAll = {
    selected: false
  }

  //return table, with a header with the data keywords
  return(
    <table>
      <thead className="tableHeader">
        <tr>
          {
            selectTable ? 
              <CheckboxColumn 
                dataEntry={selectAll} 
                onChange={checkAllChange}
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
const CheckboxColumn = ({dataEntry, onChange, data}) => {
  return (
    <td className="checkboxColumn"> 
      <input 
        type="checkbox" 
        checked={dataEntry?.selected} 
        onChange={onChange.bind(null, dataEntry, data)}/>
    </td>
  );
}

function checkboxChange(dataEntry) {
  dataEntry.selected = !dataEntry.selected;
  handleSelectionChanged();
}

function checkAllChange(dataEntry, data) {
  dataEntry.selected = !dataEntry.selected;
  if (dataEntry.selected) {
    data.forEach(element => {
      element.selected = true;
    });
  } else {
    data.forEach(element => {
      element.selected = false;
    });
  }
}

function handleSelectionChanged(){

}

export default DisplayTable;
