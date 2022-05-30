import React, { useContext, useState, useEffect } from 'react'
import GetUniqueCategories from '../../pages/visualizations/single_visualization/utils/GetUniqueCategories'
import cleanFetchedData from './DataParsing'
import structServerData from './structServer.json'

export const DataContext = React.createContext()
export const StructureContext = React.createContext()
export const SelectedContext = React.createContext()
export const CheckedContext = React.createContext()
export const CheckedContextUpdate = React.createContext()
export const ColumnSelectionContext = React.createContext()
export const ColumnSelectionContextUpdate = React.createContext()
export const VisualsContext = React.createContext()
export const VisualsUpdateContext = React.createContext()

export function useData() {
  return useContext(DataContext)
}

export function useStructure() {
  return useContext(StructureContext)
}

export function useSelectedData() {
  return useContext(SelectedContext)
}

export function useCheckedState() {
  return useContext(CheckedContext)
}

export function useCheckedStateUpdate() {
  return useContext(CheckedContextUpdate)
}

export function useColumnSelection() {
  return useContext(ColumnSelectionContext)
}

export function useColumnSelectionUpdate() {
  return useContext(ColumnSelectionContextUpdate)
}

export function useVisuals() {
  return useContext(VisualsContext)
}

export function useVisualsUpdate() {
  return useContext(VisualsUpdateContext)
}

export function DataProvider({ children }) {
  // list of all the medicine data points
  const [medData, setMedData] = useState([])

  // json object defining the structure of the fetched medicine data
  const [structData, setStructData] = useState({})

  // retrieve all medicine data points from the backend
  useEffect(() => {
    async function fetchAllData() {
      const medResponse = await fetch(
        `${process.env.PUBLIC_URL}/api/medicine/`,
        {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        }
      )
      const structResponse = await fetch(
        `${process.env.PUBLIC_URL}/api/detailedData/`,
        {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        }
      )
      const structResponseData = await structResponse.json()
      //const structResponseData = structServerData
      const medResponseData = await medResponse.json()

      setMedData(cleanFetchedData(medResponseData, structResponseData))
      setStructData(structResponseData)
      console.log('fetched the data!')
    }
    fetchAllData()
  }, [setMedData])

  return (
    <StaticDataProvider allData={medData} structData={structData}>
      {children}
    </StaticDataProvider>
  )
}

export function StaticDataProvider({ children, allData, structData }) {
  //list of checked datapoints
  const [checkedState, setCheckedState] = useState(
    Object.assign({}, ...allData.map((entry) => ({ [entry.EUNoShort]: true })))
  )

  // update the checked datapoints state when the allData state is changed
  useEffect(() => {
    setCheckedState(
      Object.assign(
        {},
        ...allData.map((entry) => ({ [entry.EUNoShort]: true }))
      )
    )
  }, [allData])

  //selected datalist
  const selectedData = allData.filter((item, index) => {
    return checkedState[item.EUNoShort]
  })

  //the column selection state with the default columns on key names
  const [columnSelection, setColumnSelection] = useState([
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
  ])

  // visualisation context to save the visualisations when navigating the page
  const [visuals, setVisuals] = useState([])

  // update the visualisation context state when the allData state is changed
  useEffect(() => {
    if (allData.length > 0) {
      let uniqueCategories = GetUniqueCategories(allData)
      setVisuals([{
        id: 1,
        chartType: 'bar',
        chartSpecificOptions: {
          xAxis: 'DecisionYear',
          yAxis: 'Rapporteur',
          categoriesSelectedY: uniqueCategories['Rapporteur'],
          categoriesSelectedX: uniqueCategories['DecisionYear'],
        },
        legendOn: false,
        labelsOn: false,
      }])
    }
  }, [allData])

  return (
    <DataContext.Provider value={allData}>
      <StructureContext.Provider value={structData}>
        <SelectedContext.Provider value={selectedData}>
          <CheckedContext.Provider value={checkedState}>
            <CheckedContextUpdate.Provider value={setCheckedState}>
              <ColumnSelectionContext.Provider value={columnSelection}>
                <ColumnSelectionContextUpdate.Provider
                  value={setColumnSelection}
                >
                  <VisualsContext.Provider value={visuals}>
                    <VisualsUpdateContext.Provider value={setVisuals}>
                      {children}
                    </VisualsUpdateContext.Provider>
                  </VisualsContext.Provider>
                </ColumnSelectionContextUpdate.Provider>
              </ColumnSelectionContext.Provider>
            </CheckedContextUpdate.Provider>
          </CheckedContext.Provider>
        </SelectedContext.Provider>
      </StructureContext.Provider>
    </DataContext.Provider>
  )
}
