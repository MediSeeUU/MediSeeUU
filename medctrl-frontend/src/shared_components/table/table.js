import React from 'react';
import './table.css';
import Menu from '../menu/menu';

class Table extends React.Component {
  constructor(props) {
    super(props);
    this.state = {data: props.data}
  }

  dataToHTML() {
    return this.state.data.map(
      (entry, index1) => {
        return(
          <tr key={index1}>
            {Object.values(entry).map((propt, index2) => { return( <td key={index2}>{propt}</td> ) })}
          </tr>
        )
      }
    );
  }

  setData = (updatedData) => {
    this.setState({
      data: updatedData
    })
  }

  render() {
    return(
      <div>
        <Menu cachedData={this.props.data} updateTable={this.setData} />
        <table>
          <thead className="tableHeader">
            <tr>
              {this.state.data.length > 0 && Object.keys(this.state.data[0]).map((key, index) => { return( <th key={index}>{key}</th> ) })}
            </tr>
          </thead>
            <tbody className="tableBody">{this.dataToHTML()}</tbody>
        </table>
      </div>
    );
  }
}

export default Table;
