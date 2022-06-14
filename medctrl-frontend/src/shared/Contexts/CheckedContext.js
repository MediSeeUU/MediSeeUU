import React, { useContext, useState, useEffect } from 'react'
import { useData } from './DataContext'

// Create a new React context for the checked datapoints state
const CheckedContext = React.createContext()

// Function that returns the context such that the data can be used in other components
export function useCheckedState() {
  return useContext(CheckedContext)
}

// Provider component that provides the checked state in the application
export function CheckedProvider({ children }) {
  // The data is necessary to create a checked state based on the eu numbers
  const data = useData()

  // Initialize the state which is empty as long as the data is not retrieved yet
  const [checkedState, setCheckedState] = useState([])

  // Update the checked state when all datapoints are retrieved (or updated)
  useEffect(() => {
    // Set every datapoint as selected
    setCheckedState(
      Object.assign({}, ...data.map((entry) => ({ [entry.EUNoShort]: true })))
    )
  }, [data])

  return (
    <CheckedContext.Provider value={{ checkedState, setCheckedState }}>
      {children}
    </CheckedContext.Provider>
  )
}
