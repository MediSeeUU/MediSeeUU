import './table.css';

function DisplayTable(props) {
  const htmlData = props.data.map(
    (entry, index1) => {
      return(
        <tr key={index1}>
          {Object.values(entry).map((propt, index2) => { return( <td key={index2}>{propt}</td> ) })}
        </tr>
      )
    }
  );

  return(
    <table>
      <thead class="tableHeader">
        <tr>
          {props.data.length > 0 && Object.keys(props.data[0]).map((key, index) => { return( <th key={index}>{key}</th> ) })}
        </tr>
      </thead>
        <tbody class="tableBody">{htmlData}</tbody>
    </table>
  )
}

export default DisplayTable;
