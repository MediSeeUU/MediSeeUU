// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useContext, useState } from 'react'

// Create a new React context for the column selection state of the tables
const ColumnSelectionContext = React.createContext()

// Function that returns the context such that the data can be used in other components
export function useColumnSelection() {
  return useContext(ColumnSelectionContext)
}

// Represents the default column selection
export const defaultColumns = [
  'eunumber',
  'brandname',
  'mah',
  'decisiondate',
  'atccode',
]

// Provider component that provides the column selection state in the application
export function ColumnSelectionProvider({ children }) {
  // Set the default column selection state (in order from left to right)
  const [columnSelection, setColumnSelection] = useState(defaultColumns)

  return (
    <ColumnSelectionContext.Provider
      value={{ columnSelection, setColumnSelection }}
    >
      {children}
    </ColumnSelectionContext.Provider>
  )
}
