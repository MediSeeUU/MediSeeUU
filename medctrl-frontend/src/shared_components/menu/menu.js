import React from 'react';
import ReactModal from 'react-modal';
import { v4 as uuidv4 } from 'uuid';
import MenuItem from './MenuItem';
import './Menu.css';

class Menu extends React.Component {
  constructor(props) {
    super(props);
    this.state = {showModal: false, filters: [{selected: null, input: [""]}]}
    this.handleOpenModal = this.handleOpenModal.bind(this);
    this.handleCloseModal = this.handleCloseModal.bind(this);
    this.addFilter = this.addFilter.bind(this);
    this.applyFilters = this.applyFilters.bind(this);
    this.clearFilters = this.clearFilters.bind(this);
  }
  
  handleOpenModal() {
    this.setState({ showModal: true });
  }
  
  handleCloseModal() {
    this.setState({ showModal: false });
  }

  addFilter() {
    this.setState(
      prevState => ({
        filters: prevState.filters.concat([{selected: null, input: [""]}])
      })
    );
  }

  updateElement(id, func) {
    var newFilter = this.state.filters.map(
      (obj, oid) => {
        if (oid === id) {
          return func(obj)
        }
        return obj
      }
    )
    this.setState({
      filters: newFilter
    })
  }

  addFilterBox = (id) => {
    this.updateElement(id, obj => {
      let newInput = obj.input.concat([""]);
      return {...obj, input: newInput}
    })
  }

  deleteFilterBox = (id, bid) => {
    this.updateElement(id, obj => {
      if (obj.input.length > 1) {
        let newInput = [...obj.input];
        newInput.splice(bid, 1);
        return {...obj, input: newInput}
      }
      return obj
    })
  }

  deleteFilter = (id) => {
    if (this.state.filters.length > 1) {
      let newFilter = [...this.state.filters];
      newFilter.splice(id, 1);
      this.setState({
        filters: newFilter
      });
    }
  }

  updateSelected = (id, newSelected) => {
    this.updateElement(id, obj => {
      return {...obj, selected: newSelected}
    })
  }

  updateInput = (id, index, value) => {
    this.updateElement(id, obj => {
      let newInput = [...obj.input];
      newInput[index] = value;
      return {...obj, input: newInput}
    })
  }
  
  applyFilters() {
    let filterData = this.props.cachedData;
    this.state.filters.forEach(item => {filterData = this.applyFilter(item, filterData)});
    this.props.updateTable(filterData);
    this.handleCloseModal();
  }

  applyFilter(item, data) {
    if (item.selected === null) {
      return data
    }
    return data.filter(
      obj => {
        return item.input.some(x => obj[item.selected].toString().includes(x))
      }
    )
  }

  clearFilters() {
    this.setState({
      filters: [{selected: null, input: [""]}]
    });
    this.props.updateTable(this.props.cachedData);
    this.handleCloseModal();
  }
  
  render () {
    const list = this.props.cachedData.length > 0 && Object.keys(this.props.cachedData[0]).map(item => { return( <option key={item} value={item}>{item}</option> ) });
    return (
      <div>
        <i className="bx bxs-filter-alt options" onClick={this.handleOpenModal} > Open Menu</i>
        <ReactModal className="modal" isOpen={this.state.showModal} ariaHideApp={false} contentLabel="Menu">
          <h1>Filter Menu</h1>
          <div className="mb add" onClick={this.addFilter}>
            Add Filter
            <i className="bx bxs-plus-square add-icon"></i>
          </div>
          <div className="filters">
            {this.state.filters.map((obj, oid) =>
              <MenuItem
                key={uuidv4()}
                id={oid}
                item={obj}
                options={list}
                del={this.deleteFilter}
                box={this.addFilterBox}
                dbox={this.deleteFilterBox}
                sel={this.updateSelected}
                fil={this.updateInput}
              />
            )}
          </div>
          <button className="mb apply" onClick={this.applyFilters}>Apply</button>
          <button className="mb close-clean" onClick={this.clearFilters}>Clear</button>
          <button className="mb close-clean" onClick={this.handleCloseModal}>Close</button>
        </ReactModal>
      </div>
    );
  }
}

export default Menu;
