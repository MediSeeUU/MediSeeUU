import React, { useContext, useState, useEffect } from 'react'
import GetUniqueCategories from '../../pages/visualizations/single_visualization/utils/GetUniqueCategories'
import cleanFetchedData from './DataParsing'

export const DataContext = React.createContext()
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

  // retrieve all medicine data points from the backend
  useEffect(() => {
    async function fetchAllData() {
      const response = await fetch(`${process.env.PUBLIC_URL}/api/medicine/`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
      })
      const repsonseData = await response.json()
      setMedData(cleanFetchedData(repsonseData))
    }
    fetchAllData()
  }, [setMedData])

  return (
    <StaticDataProvider allData={medData} > 
      {children}
    </StaticDataProvider>
  )
}

export function StaticDataProvider({ children, allData}) {

  //list of checked datapoints
  const [checkedState, setCheckedState] = useState(
    Object.assign({}, ...allData.map((entry) => ({ [entry.EUNumber]: true })))
  )

  // update the checked datapoints state when the allData state is changed
  useEffect(() => {
    setCheckedState(
      Object.assign({}, ...allData.map((entry) => ({ [entry.EUNumber]: true })))
    )
  }, [allData])

  //selected datalist
  const selectedData = allData.filter((item, index) => {
    return checkedState[item.EUNumber]
  })

  //the column selection state with the default columns on key names
  const [columnSelection, setColumnSelection] = useState([
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCNameL2',
  ])

  // visualisation context to save the visualisations when navigating the page
  const [visuals, setVisuals] = useState([])

  // update the visualisation context state when the allData state is changed
  useEffect(() => {
    let uniqueCategories = GetUniqueCategories(allData)
    setVisuals([
      {
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
        data: [],
        series: [],
        uniqueCategories: [],
        key: '',
      },
    ])
  }, [allData])

  return (
    <DataContext.Provider value={allData}>
      <SelectedContext.Provider value={selectedData}>
        <CheckedContext.Provider value={checkedState}>
          <CheckedContextUpdate.Provider value={setCheckedState}>
            <ColumnSelectionContext.Provider value={columnSelection}>
              <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
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
    </DataContext.Provider>
  )
}
