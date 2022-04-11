import React from 'react'
import ReactModal from 'react-modal'
import { v4 as uuidv4 } from 'uuid'
import Filter from './filter'
import OutsideClickHandler from 'react-outside-click-handler'
import './menu.css'

class Menu extends React.Component {
  constructor(props) {
    super(props)

    // Default filter object
    this.filterObject = [{ selected: '', input: [''] }]

    // Set init state
    this.state = { showModal: false, filters: this.filterObject }

    // Binding of functions
    this.handleOpenModal = this.handleOpenModal.bind(this)
    this.handleCloseModal = this.handleCloseModal.bind(this)
    this.addFilter = this.addFilter.bind(this)
    this.applyFilters = this.applyFilters.bind(this)
    this.clearFilters = this.clearFilters.bind(this)
  }

  // Opens menu
  handleOpenModal() {
    this.setState({ showModal: true })
  }

  // Closes menu
  handleCloseModal() {
    this.setState({ showModal: false })
  }

  // Adds new filter item to the menu
  addFilter() {
    this.setState((prevState) => ({
      filters: prevState.filters.concat(this.filterObject),
    }))
  }

  // Standard function to update element with given id in filters
  updateElement(id, func) {
    var newFilter = this.state.filters.map((obj, oid) => {
      if (oid === id) {
        return func(obj)
      }
      return obj
    })
    this.setState({
      filters: newFilter,
    })
  }

  // Adds a new filter input box to a filter item
  addFilterBox = (id) => {
    this.updateElement(id, (obj) => {
      let newInput = obj.input.concat([''])
      return { ...obj, input: newInput }
    })
  }

  // Deletes the specified input box of the filter item
  deleteFilterBox = (id, bid) => {
    this.updateElement(id, (obj) => {
      if (obj.input.length > 1) {
        let newInput = [...obj.input]
        newInput.splice(bid, 1)
        return { ...obj, input: newInput }
      }
      return obj
    })
  }

  // Deletes specified filter item from the menu
  deleteFilter = (id) => {
    if (this.state.filters.length > 1) {
      let newFilter = [...this.state.filters]
      newFilter.splice(id, 1)
      this.setState({
        filters: newFilter,
      })
    }
  }

  // Updates the selected item of the specified filter item
  updateSelected = (id, newSelected) => {
    this.updateElement(id, (obj) => {
      return { ...obj, selected: newSelected }
    })
  }

  // Updates the specified input box value of the specified filter item
  updateInput = (id, index, value) => {
    this.updateElement(id, (obj) => {
      let newInput = [...obj.input]
      newInput[index] = value
      return { ...obj, input: newInput }
    })
  }

  // Applies all filters to the cached data, updates the table with this updated data and closes menu
  applyFilters() {
    let filterData = this.props.cachedData
    this.state.filters.forEach((item) => {
      filterData = this.applyFilter(item, filterData)
    })
    this.props.updateTable(filterData)
    this.handleCloseModal()
  }

  // Single filter that returns the updated data given the filter item
  applyFilter(item, data) {
    if (!item.selected) {
      return data
    }
    return data.filter((obj) => {
      return item.input.some((x) => obj[item.selected].toString().includes(x))
    })
  }

  // Resets the filter menu, updates the table with the cached data and closes menu
  clearFilters() {
    this.setState({
      filters: this.filterObject,
    })
    this.props.updateTable(this.props.cachedData)
    this.handleCloseModal()
  }

  render() {
    // List of options which will be used in every select of a filter item
    const list =
      this.props.cachedData.length > 0 &&
      Object.keys(this.props.cachedData[0]).map((item) => {
        return (
          <option key={item} value={item}>
            {item}
          </option>
        )
      })
    // Returns the menu in HTML
    return (
      <div>
        <label>Active table settings</label>
        <button className="tableButtons" onClick={this.handleOpenModal}>
          <i className="bx bx-cog filter-Icon"></i>Filter & Sort
        </button>
        <hr></hr>
        <ReactModal
          className="menu-modal"
          isOpen={this.state.showModal}
          ariaHideApp={false}
          contentLabel="Menu"
        >
          <h1 className="filter-header">Filter Menu</h1>
          <div className="menu-button add" onClick={this.addFilter}>
            Add Filter
            <i className="bx bxs-plus-square add-icon"></i>
          </div>
          <div className="filters">
            {this.state.filters.map((obj, oid) => (
              <Filter
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
            ))}
          </div>
          <button className="menu-button apply" onClick={this.applyFilters}>
            Apply
          </button>
          <button className="menu-button cl" onClick={this.clearFilters}>
            Clear
          </button>
          <button className="menu-button cl" onClick={this.handleCloseModal}>
            Close
          </button>
        </ReactModal>
      </div>
    )
  }
}

export default Menu
