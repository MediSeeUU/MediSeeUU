import React, { useContext, useState, useEffect } from 'react'

const StructureContext = React.createContext()

export function useStructure() {
  return useContext(StructureContext)
}

export function StructureProvider({ children }) {
  // json object defining the structure of the fetched medicine data
  const [structData, setStructData] = useState(null)

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
    fetchData()
  }, [setStructData])

  return (
    <StructureContext.Provider value={structData}>
      {children}
    </StructureContext.Provider>
  )
}
