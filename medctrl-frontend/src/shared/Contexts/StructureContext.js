import React, { useContext, useState, useEffect } from 'react'

// Create a new React context for the structure data
// The structure is used to determine the variables that can be selected
// And how the data must be formatted
const StructureContext = React.createContext()

// Function that returns the context such that the data can be used in other components
export function useStructure() {
  return useContext(StructureContext)
}

// Provider component that provides the structure data in the application
export function StructureProvider({ mock, children }) {
  // Initialize the structure data which is empty as long as the data is not retrieved yet
  const [structData, setStructData] = useState(null)

  // Update the state if the structure data is retrieved from the API
  useEffect(() => {
    async function fetchData() {
      const structResponse = await fetch(
        `${process.env.PUBLIC_URL}/api/detailedData/`,
        {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        }
      )
      const structResponseData = await structResponse.json()
      setStructData(structResponseData)
    }

    // The update will only happen if the provider is not being mocked
    if (!mock) {
      fetchData()
    }
  }, [setStructData, mock])

  // Provide the mock data if this is given, otherwise the obtained structure data
  return (
    <StructureContext.Provider value={mock || structData}>
      {children}
    </StructureContext.Provider>
  )
}
