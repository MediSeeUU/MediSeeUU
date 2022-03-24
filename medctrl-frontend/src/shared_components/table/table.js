import './table.css';

//function based component, returns table
function DisplayTable({data, selectTable}) {
  //constant with the table body data, for every data entry add a new row
  const htmlData = data.map(
    (entry, index1) => {
      return(
        <tr key={index1}>
          {
            selectTable ? 
              <checkboxColumn 
                dataEntry={entry} 
                onChange={checkboxChange}/> 
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
          {selectTable ? <th className="checkboxColumn"><Checkbox/></th> : null}
          {data.length > 0 && Object.keys(data[0]).map((key, index) => { return( <th key={index}>{key}</th> ) })}
        </tr>
      </thead>
        <tbody className="tableBody">{htmlData}</tbody>
    </table>
  )
}

//checkbox for the selection table
const checkboxColumn = ({dataEntry, onChange}) => {
  return (
    <td className="checkboxColumn"> 
      <input 
        type="checkbox" 
        selected={dataEntry?.selected} 
        onChange={onChange.bind(null, dataEntry)}/>
    </td>
  );
}

function checkboxChange(dataEntry) {
  dataEntry.selected = !dataEntry.selected;
  handleSelectionChanged();
}

function checkAllChange(dataEntry) {

}

function handleSelectionChanged(){
  
}

export default DisplayTable;
