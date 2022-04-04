import React from 'react'
import ReactModal from 'react-modal'
import { v4 as uuidv4 } from 'uuid'
import Filter from './filter'
import Sort from './sort'
import './menu.css'

class Menu extends React.Component {
  constructor(props) {
    super(props)

    // Default filter object
    this.filterObject = [{ selected: '', input: [''] }]
    this.sortObject = [{selected: '', order: 'asc'}]

    // Set init state
    this.state = { showModal: false, filters: this.filterObject, sorters: this.sortObject, showAddSort: true }

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

  // Standard function to update element with given id in sorters
  updateSortElement(id, func) {
    var newSorters = this.state.sorters.map((obj, oid) => {
      if (oid === id) {
        return func(obj)
      }
      return obj
    })
    this.setState({
      sorters: newSorters,
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

  // Applies all filters and sorters to the cached data, updates the table with this updated data and closes menu
  apply() {
    let filterData = this.props.cachedData
    this.state.filters.forEach((item) => {
      filterData = this.applyFilter(item, filterData)
    })

    // Hier komt sorteer functie

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

  // Resets the filter and sort menu, updates the table with the cached data and closes menu
  clear() {
    this.setState({
      filters: this.filterObject,
      sorters: this.sortObject,
    })
    this.props.updateTable(this.props.cachedData)
    this.handleCloseModal()
  }

  // Adds new sort item to the menu (max 5)
  addSort() {
    this.setState((prevState) => ({
      sorters: prevState.sorters.concat(this.sortObject),
    }))
    if (this.state.sorters.length >= 4) {
      this.setState({showAddSort: false})
    }
  }

  // Deletes specified sort item from the menu
  deleteSort = (id) => {
    if (this.state.sorters.length > 1) {
      let newSorters = [...this.state.sorters]
      newSorters.splice(id, 1)
      this.setState({
        sorters: newSorters,
      })
    }
    this.setState({showAddSort: true})
  }

  updateSelectSort = (id, newSelected) => {
    this.updateSortElement(id, (obj) => {
      return { ...obj, selected: newSelected }
    })
  }

  updateSortingOrder = (id, newOrder) => {
    this.updateSortElement(id, (obj) => {
      return { ...obj, order: newOrder }
    })
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
        <i
          className="bx bxs-filter-alt open-menu"
          onClick={this.handleOpenModal}
        >
          {' '}
          Open Menu
        </i>
        <ReactModal
          className="modal"
          isOpen={this.state.showModal}
          ariaHideApp={false}
          contentLabel="Menu"
        >
          <div className="filter">
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
            <button className="menu-button apply" onClick={this.apply}>
              Apply
            </button>
            <button className="menu-button cl" onClick={this.clear}>
              Clear
            </button>
            <button className="menu-button cl" onClick={this.handleCloseModal}>
              Close
            </button>
          </div>
          <div className="sort">
            <h1 className="filter-header">Sort</h1>
            {this.state.sorters.map((obj, oid) => (
                <Sort
                  key={uuidv4()}
                  id={oid}
                  item={obj}
                  options={list}
                  del={this.deleteSort}
                  sel={this.updateSelectSort}
                  order={this.updateSortingOrder}
                />
              ))}
            {this.state.showAddSort && <label className="add-sort" onClick={this.addSort}>Add Sorting option +</label>}
          </div>
        </ReactModal>
      </div>
    )
  }
}

export default Menu
