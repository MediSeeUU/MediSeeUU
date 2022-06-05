import React, { useContext, useState, useEffect } from 'react'
import cleanFetchedData from './format'
import { useStructure } from './StructureContext'

export const DataContext = React.createContext()

export function useData() {
  return useContext(DataContext)
}

export function DataProvider({ children }) {
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
    fetchData()
  }, [structData, setData])

  return <DataContext.Provider value={data}>{children}</DataContext.Provider>
}
