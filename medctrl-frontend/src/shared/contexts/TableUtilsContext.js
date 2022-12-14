// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useContext, useState } from 'react'

// Create a new React context for the table utils data
// This is used to store the applied search, filters and sorters
const TableUtilsContext = React.createContext()

// Function that returns the context such that the data can be used in other components
export function useTableUtils() {
  return useContext(TableUtilsContext)
}

// Provider component that provides the table utils data in the application
export function TableUtilsProvider({ children }) {
  // Initialize the state with an empty query and one unspecified filter and sorter item
  const [tableUtils, setTableUtils] = useState({
    search: '',
    filters: [
      {
        selected: '',
        input: [{ var: '', filterRange: 'from', custom: true }],
        filterType: '',
      },
    ],
    sorters: [{ selected: '', order: 'asc' }],
  })

  return (
    <TableUtilsContext.Provider value={{ tableUtils, setTableUtils }}>
      {children}
    </TableUtilsContext.Provider>
  )
}
