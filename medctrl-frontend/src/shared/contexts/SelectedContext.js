// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useContext } from 'react'
import { useCheckedState } from './CheckedContext'
import { useData } from './DataContext'

// Create a new React context for the selected medicines data
// The application uses this data to visualize the selected datapoints in the table and charts
export const SelectedContext = React.createContext()

// Function that returns the context such that the data can be used in other components
export function useSelectedData() {
  return useContext(SelectedContext)
}

// Provider component that provides the selected medicines data in the application
export function SelectedProvider({ children }) {
  // We need the data and the current checked state
  const data = useData()
  const { checkedState } = useCheckedState()

  // Initialize the state with the selected datapoints
  const selectedData = data.filter((item, _) => {
    return checkedState[item.eu_pnumber]
  })

  return (
    <SelectedContext.Provider value={selectedData}>
      {children}
    </SelectedContext.Provider>
  )
}
