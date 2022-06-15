// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import { v4 as uuidv4 } from 'uuid'
import Sort from './Sort'

// Function based component which renders the sort menu
function SortMenu({ sorters, setSorters, defaultObj }) {
  // Add sort item to the menu
  const addSort = () => setSorters(sorters.concat(defaultObj))

  // Generic function to update the sort object
  // This is used by the other functions here
  const updateSorter = (id, func) => {
    const newSorters = sorters.map((obj, oid) => {
      if (oid === id) {
        return func(obj)
      }
      return obj
    })
    setSorters(newSorters)
  }

  // Deletes specified sort item from the menu
  const deleteSort = (id) => {
    let newSorters = [...sorters]
    newSorters.splice(id, 1)
    setSorters(newSorters)
  }

  // Updates the selected item of the specified sort item
  const updateSortSelected = (id, newSelected) => {
    updateSorter(id, (obj) => {
      return { ...obj, selected: newSelected }
    })
  }

  // Updates the sorting order of the specified sort item
  const updateSortOrder = (id, newOrder) => {
    updateSorter(id, (obj) => {
      return { ...obj, order: newOrder }
    })
  }

  return (
    <div className="med-sort-menu">
      <h1 className="med-table-menu-header">Sort</h1>
      <hr className="med-top-separator" />
      <div className="med-table-menu-sort-container">
        {sorters.map((obj, oid) => (
          <Sort
            key={uuidv4()}
            id={oid}
            item={obj}
            del={deleteSort}
            sel={updateSortSelected}
            order={updateSortOrder}
          />
        ))}
        {sorters.length < 4 && (
          <label
            className="med-able-menu-add-sort-button med-primary-text"
            onClick={addSort}
          >
            Add Sorting option +
          </label>
        )}
      </div>
    </div>
  )
}

export default SortMenu
