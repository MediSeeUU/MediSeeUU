import React from 'react'
import ReactModal from 'react-modal'
import { v4 as uuidv4 } from 'uuid'
import Filter from './Filter'
import Sort from './Sort'
import './Menu.css'

class Menu extends React.Component {
  constructor(props) {
    super(props)

    // Default filter and sort objects
    this.filterObject = [
      {
        selected: '',
        input: [{ var: '', filterRange: 'from' }],
        filterType: '',
      },
    ]
    this.sortObject = [{ selected: '', order: 'asc' }]

    // Set init state
    this.state = {
      showModal: false,
      filters: props.filters,
      sorters: props.sorters,
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
      let newInput = obj.input.concat({ var: '', filterRange: 'from' })
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
      return { ...obj, input: [{ var: '', filterRange: 'from' }] }
    })
  }

  // Deletes specified filter item from the menu
  deleteFilter = (id) => {
    this.removeElement('filters', id)
  }

  // Deletes specified sort item from the menu
  deleteSort = (id) => {
    this.removeElement('sorters', id)
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
    this.props.update(this.state.filters, this.state.sorters)
    this.handleCloseModal()
  }

  // Update the filters and sorters which will update the data displayed in the table
  clear() {
    this.props.update(this.state.filters, this.state.sorters)
    this.setState({
      filters: this.filterObject,
      sorters: this.sortObject,
    })
    this.handleCloseModal()
  }

  render() {
    return (
      <>
        <button
          className="med-primary-solid med-bx-button med-data-button"
          onClick={this.handleOpenModal}
        >
          <i className="bx bx-cog med-button-image"></i>Filter & Sort
        </button>

        <ReactModal
          className="med-table-menu-modal"
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
          <div className="med-filter-menu">
            <h1 className="med-table-menu-header">Filters</h1>
            <hr className="med-top-separator" />
            <div
              className="med-table-menu-add-filter med-primary-text"
              onClick={this.addFilter}
            >
              Add Filter
              <i className="bx bxs-plus-square med-table-menu-add-filter-icon"></i>
            </div>
            <div className="med-table-menu-filters-container">
              {this.state.filters.map((filter, index) => (
                <Filter
                  key={uuidv4()}
                  id={index}
                  item={filter}
                  del={this.deleteFilter}
                  box={this.addFilterBox}
                  dbox={this.deleteFilterBox}
                  sel={this.updateFilterSelected}
                  fil={this.updateFilterInput}
                />
              ))}
            </div>
            <div className="med-table-menu-filter-button-container">
              <button
                className="med-table-menu-button med-table-menu-apply-button med-primary-solid"
                onClick={this.apply}
              >
                Apply
              </button>
              <button
                className="med-table-menu-button med-table-menu-secondary-button"
                onClick={this.clear}
              >
                Clear
              </button>
              <button
                className="med-table-menu-button med-table-menu-secondary-button"
                onClick={this.handleCloseModal}
              >
                Close
              </button>
            </div>
          </div>
          <div className="med-sort-menu">
            <h1 className="med-table-menu-header">Sort</h1>
            <hr className="med-top-separator" />
            <div className="med-table-menu-sort-container">
              {this.state.sorters.map((obj, oid) => (
                <Sort
                  key={uuidv4()}
                  id={oid}
                  item={obj}
                  del={this.deleteSort}
                  sel={this.updateSortSelected}
                  order={this.updateSortOrder}
                />
              ))}
              {this.state.sorters.length < 4 && (
                <label
                  className="med-able-menu-add-sort-button med-primary-text"
                  onClick={this.addSort}
                >
                  Add Sorting option +
                </label>
              )}
            </div>
          </div>
        </ReactModal>
      </>
    )
  }
}

export default Menu
