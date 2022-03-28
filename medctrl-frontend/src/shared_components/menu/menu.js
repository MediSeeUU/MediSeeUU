import React from 'react';
import ReactModal from 'react-modal';
import MenuItem from './MenuItem';
import './menu.css';

class Menu extends React.Component {
  constructor(props) {
    super(props);
    this.state = {showModal: false, filters: [{id: 0, selected: "ApplicationNo", input: ""}], fIndex: 1}
    this.handleOpenModal = this.handleOpenModal.bind(this);
    this.handleCloseModal = this.handleCloseModal.bind(this);
  }
  
  handleOpenModal () {
    this.setState({ showModal: true });
  }
  
  handleCloseModal () {
    this.setState({ showModal: false });
  }

  addFilter = () => {
    this.setState(
      prevState => ({
        filters: prevState.filters.concat([{id: prevState.fIndex, selected: "ApplicationNo", input: ""}]),
        fIndex: prevState.fIndex + 1
      })
    );
  }

  deleteFilter = (id) => {
    if (this.state.filters.length > 1) {
      var updatedFilter = this.state.filters.filter(
        obj => {
          return obj.id !== id
        }
      );
      this.setState({
        filters: updatedFilter
      });
    }
  }

  updateFilter = (id, newInput, selectedChanged) => {
    var updatedFilter = this.state.filters.map(
      obj => {
        if (obj.id === id) {
          if (selectedChanged) {
            return {...obj, selected: newInput};
          }
          return {...obj, input: newInput};
        }
        return obj;
      }
    );
    this.setState({
      filters: updatedFilter
    });
  }
  
  applyFilters() {
    var filterData = this.props.cachedData;
    this.state.filters.forEach(item => {filterData = this.applyFilter(item, filterData)});
    this.props.updateTable(filterData);
    this.handleCloseModal();
  }

  applyFilter(item, data) {
    return (
      data.filter(
        obj => {
          return obj[item.selected].toString().includes(item.input)
        }
      )
    );
  }

  clearFilters() {
    this.setState({
      filters: [{id: 0, selected: "ApplicationNo", input: ""}],
      fIndex: 1
    });
    this.props.updateTable(this.props.cachedData);
    this.handleCloseModal();
  }
  
  render () {
    const list = this.props.cachedData.length > 0 && Object.keys(this.props.cachedData[0]).map(key => { return( <option value={key}>{key}</option> ) });
    return (
      <div>
        <i className="bx bxs-filter-alt options" onClick={this.handleOpenModal} > Filter</i>
        <ReactModal className="modal" isOpen={this.state.showModal} ariaHideApp={false}>
          <h1>Filter Menu</h1>
          <i className="bx bx-exit mb close" onClick={this.handleCloseModal}></i>
          <button className="mb apply" onClick={() => this.applyFilters()}>Apply</button>
          <button className="mb clear" onClick={() => this.clearFilters()}>Clear</button>
          {this.state.filters.map(item => <MenuItem id={item.id} selected={item.selected} input={item.input} options={list} add={this.addFilter} del={this.deleteFilter} update={this.updateFilter} />)}
        </ReactModal>
      </div>
    );
  }
}

export default Menu;
