import React from 'react'
import ReactModal from 'react-modal'
import { v4 as uuidv4 } from 'uuid'
import Filter from './Filter'
import Sort from './Sort'
import './Menu.css'

class Menu extends React.Component {
  constructor(props) {
    super(props)

    // Default filter object
    this.filterObject = [{ selected: '', input: [{var: '', filterRange: 'from'}] }]
    this.sortObject = [{ selected: '', order: 'asc' }]

    // Set init state
    this.state = {
      showModal: false,
      filters: props.filters,
      sorters: props.sorters,
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
    console.log(this.filterObject)
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
      let newInput = obj.input.concat({var: '', filterRange: 'from'})
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
      return { ...obj, input: [{var: '', filterRange: 'from'}] }
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
      return { ...obj, selected: newSelected}
    })
  }

  // Updates the specified input box value of the specified filter item
  updateFilterInput = (id, index, value) => {
    this.updateElement('filters', id, (obj) => {
      let newInput = [...obj.input]
      newInput[index].var = value
      
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

  // Update the filters and sorters which will update the data displayed in the table
  apply() {
    this.props.updateFilters(this.state.filters)
    this.props.updateSorters(this.state.sorters)
    this.handleCloseModal()
  }

  // Update the (local) filters and sorters which will update the data displayed in the table
  clear() {
    this.props.updateFilters([{ selected: '', input: [{var: '', filterRange:'from'}], filterType: '' }])
    this.props.updateSorters([{ selected: '', order: 'asc' }])
    this.setState({
      filters: this.filterObject,
      sorters: this.sortObject,
      showAddSort: true,
    })
    this.handleCloseModal()
  }

  render() {
    // Returns the menu in HTML
    return (
      <>
        <button
          className="med-primary-solid med-bx-button"
          onClick={this.handleOpenModal}
        >
          <i className="bx bx-cog filter-Icon"></i>Filter & Sort
        </button>


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
            <hr className="med-top-separator" />
            <div className="add med-primary-text" onClick={this.addFilter}>
              Add Filter
              <i className="bx bxs-plus-square add-icon"></i>
            </div>
            <div className="filters">
              {console.log(this.props.list)}
              {this.state.filters.map((filter, index) => (
                <Filter
                  key={uuidv4()}
                  id={index}
                  item={filter}
                  options={this.props.list}
                  del={this.deleteFilter}
                  box={this.addFilterBox}
                  dbox={this.deleteFilterBox}
                  sel={this.updateFilterSelected}
                  fil={this.updateFilterInput}
                />
              ))}
              {console.log(this.state.filters)}
            </div>
            <div className="filter-bttn-box">
              <button
                className="menu-button apply med-primary-solid"
                onClick={this.apply}
              >
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
            <hr className="med-top-separator" />
            {this.state.sorters.map((obj, oid) => (
              <Sort
                key={uuidv4()}
                id={oid}
                item={obj}
                options={this.props.list}
                del={this.deleteSort}
                sel={this.updateSortSelected}
                order={this.updateSortOrder}
              />
            ))}
            {this.state.showAddSort && (
              <label
                className="add-sort med-primary-text"
                onClick={this.addSort}
              >
                Add Sorting option +
              </label>
            )}
          </div>
        </ReactModal>
      </>
    )
  }
}

export default Menu
