// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import React, { useContext, useState, useEffect } from 'react'
import cleanFetchedData from './format'
import { useStructure } from './StructureContext'

// Create a new React context for the medicines data
const DataContext = React.createContext()

// Function that returns the context such that the data can be used in other components
export function useData() {
  return useContext(DataContext)
}

// Provider component that provides the medicines data in the application
export function DataProvider({ mock, children }) {
  // The structure data is needed to transform the data
  const structData = useStructure()

  // Initialize the state which is empty as long as the data is not retrieved yet
  const [data, setData] = useState([])

  // Update the state if the medicines data is fetched from the API
  useEffect(() => {
    async function fetchData() {
      const medResponse = await fetch(
        `${process.env.PUBLIC_URL}/api/medicine/`,
        {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        }
      )

      const medResponseData = await medResponse.json()
      setData(cleanFetchedData(medResponseData, structData))
    }

    // The update will only happen if the structure data is retrieved already
    // And the provider is not being mocked
    if (structData && !mock) {
      fetchData()
    }
  }, [structData, setData, mock])

  // Provide the mock data if this is given, otherwise the obtained medicines data
  return (
    <DataContext.Provider value={mock || data}>{children}</DataContext.Provider>
  )
}
