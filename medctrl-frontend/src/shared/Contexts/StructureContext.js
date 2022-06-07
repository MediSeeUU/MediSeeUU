import React, { useContext, useState, useEffect } from 'react'

const StructureContext = React.createContext()

export function useStructure() {
  return useContext(StructureContext)
}

export function StructureProvider({ mock, children }) {
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

    if (!mock) {
      fetchData()
      console.log("fetched structure data")
    }
  }, [setStructData, mock])

  return (
    <StructureContext.Provider value={mock || structData}>
      {children}
    </StructureContext.Provider>
  )
}
