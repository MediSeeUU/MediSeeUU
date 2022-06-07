import React, { useContext, useState, useEffect } from 'react'
import cleanFetchedData from './format'
import { useStructure } from './StructureContext'

const DataContext = React.createContext()

export function useData() {
  return useContext(DataContext)
}

export function DataProvider({ mock, children }) {
  const structData = useStructure()

  // list of all the medicine data points
  const [data, setData] = useState([])

  // retrieve all medicine data points from the backend
  useEffect(() => {
    async function fetchData() {
      const medResponse = await fetch(
        `${process.env.PUBLIC_URL}/api/medicine/`,
        {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        }
      )

      //const structResponseData = structServerData
      const medResponseData = await medResponse.json()
      setData(cleanFetchedData(medResponseData, structData))
    }

    if (!mock) {
      fetchData()
      console.log("fetched medicines data")
    }
  }, [structData, setData, mock])

  return <DataContext.Provider value={mock || data}>{children}</DataContext.Provider>
}
