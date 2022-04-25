import React from 'react'
import ReactModal from 'react-modal'
import { v4 as uuidv4 } from 'uuid'
import Filter from './filter'
import Sort from './sort'
import './menu.css'
import { sortData } from './sorting'

class Menu extends React.Component {
  constructor(props) {
    super(props)

    // Default filter object
    this.filterObject = [{ selected: '', input: [''] }]
    this.sortObject = [{ selected: '', order: 'asc' }]

    // Set init state
    this.state = {
      showModal: false,
      filters: this.filterObject,
      sorters: this.sortObject,
      showAddSort: true,
    }

    // Binding of functions
    this.handleOpenModal = this.handleOpenModal.bind(this)
    this.handleCloseModal = this.handleCloseModal.bind(this)
    this.addFilter = this.addFilter.bind(this)
    this.addSort = this.addSort.bind(this)
    this.apply = this.apply.bind(this)
    this.clear = this.clear.bind(this)
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

  // Adds new sort item to the menu (max 4)
  addSort() {
    this.setState((prevState) => ({
      sorters: prevState.sorters.concat(this.sortObject),
    }))
    if (this.state.sorters.length >= 3) {
      this.setState({ showAddSort: false })
    }
  }

  // Standard function to update element in state with given id in property
  updateElement(propertyName, id, func) {
    var newFilter = this.state[propertyName].map((obj, oid) => {
      if (oid === id) {
        return func(obj)
      }
      return obj
    })
    this.setState({
      [propertyName]: newFilter,
    })
  }

  // Standard function to remove element in state with given id in property
  removeElement(propertyName, id) {
    let updated = [...this.state[propertyName]]
    updated.splice(id, 1)
    this.setState({
      [propertyName]: updated,
    })
  }

  // Adds a new filter input box to a filter item
  addFilterBox = (id) => {
    this.updateElement('filters', id, (obj) => {
      let newInput = obj.input.concat([''])
      return { ...obj, input: newInput }
    })
  }

  // Deletes the specified input box of the filter item
  deleteFilterBox = (id, bid) => {
    this.updateElement('filters', id, (obj) => {
      if (obj.input.length > 1) {
        let newInput = [...obj.input]
        newInput.splice(bid, 1)
        return { ...obj, input: newInput }
      }
      return { ...obj, input: [''] }
    })
  }

  // Deletes specified filter item from the menu
  deleteFilter = (id) => {
    this.removeElement('filters', id)
  }

  // Deletes specified sort item from the menu
  deleteSort = (id) => {
    this.removeElement('sorters', id)
    this.setState({ showAddSort: true })
  }

  // Updates the selected item of the specified filter item
  updateFilterSelected = (id, newSelected) => {
    this.updateElement('filters', id, (obj) => {
      return { ...obj, selected: newSelected }
    })
  }

  // Updates the specified input box value of the specified filter item
  updateFilterInput = (id, index, value) => {
    this.updateElement('filters', id, (obj) => {
      let newInput = [...obj.input]
      newInput[index] = value
      return { ...obj, input: newInput }
    })
  }

  // Updates the selected item of the specified sort item
  updateSortSelected = (id, newSelected) => {
    this.updateElement('sorters', id, (obj) => {
      return { ...obj, selected: newSelected }
    })
  }

  // Updates the sorting order of the specified sort item
  updateSortOrder = (id, newOrder) => {
    this.updateElement('sorters', id, (obj) => {
      return { ...obj, order: newOrder }
    })
  }

  // Applies all filters and sorters to the cached data, updates the table with this updated data and closes menu
  apply() {
    let filterData = [...this.props.cachedData]
    this.state.filters.forEach((item) => {
      filterData = this.applyFilter(item, filterData)
    })
    let sorters = [...this.state.sorters]
    let sortedData = sortData(filterData, sorters)
    this.props.updateTable(sortedData)
    this.handleCloseModal()
  }

  // Single filter that returns the updated data given the filter item
  applyFilter(item, data) {
    if (!item.selected) {
      return data
    }
    return data.filter((obj) => {
      return item.input.some((x) =>
        obj[item.selected].toString().toLowerCase().includes(x.toLowerCase())
      )
    })
  }

  // Resets the filter and sort menu, updates the table with the cached data and closes menu
  clear() {
    this.setState({
      filters: this.filterObject,
      sorters: this.sortObject,
      showAddSort: true,
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
          onRequestClose={this.handleCloseModal}
          ariaHideApp={false}
          contentLabel="Menu"
          style={{
            modal: {},
            overlay: {
              background: 'rgba(0, 0, 0, 0.2)',
              backdropFilter: 'blur(2px)',
            },
          }}
        >
          <div className="filter">
            <h1 className="header">Filters</h1>
            <hr></hr>
            <div className="add" onClick={this.addFilter}>
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
                  sel={this.updateFilterSelected}
                  fil={this.updateFilterInput}
                />
              ))}
            </div>
            <div className="filter-bttn-box">
              <button className="menu-button apply" onClick={this.apply}>
                Apply
              </button>
              <button className="menu-button cl" onClick={this.clear}>
                Clear
              </button>
              <button
                className="menu-button cl"
                onClick={this.handleCloseModal}
              >
                Close
              </button>
            </div>
          </div>
          <div className="sort">
            <h1 className="header">Sort</h1>
            <hr></hr>
            {this.state.sorters.map((obj, oid) => (
              <Sort
                key={uuidv4()}
                id={oid}
                item={obj}
                options={list}
                del={this.deleteSort}
                sel={this.updateSortSelected}
                order={this.updateSortOrder}
              />
            ))}
            {this.state.showAddSort && (
              <label className="add-sort" onClick={this.addSort}>
                Add Sorting option +
              </label>
            )}
          </div>
        </ReactModal>
      </div>
    )
  }
}

export default Menu
