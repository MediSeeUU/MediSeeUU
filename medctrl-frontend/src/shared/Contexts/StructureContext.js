import React, { useContext, useState, useEffect } from 'react'
import structServerData from '../../json/structServer.json'

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

    if (mock) {
      setStructData(structServerData)
    }
    else {
      fetchData()
      console.log("fetched structure data")
    }
  }, [setStructData, mock])

  return (
    <StructureContext.Provider value={structData}>
      {children}
    </StructureContext.Provider>
  )
}
