import React, { useContext, useState } from 'react'
import allData from '../../testJson/data.json'

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

export function useVisuals(){
  return useContext(VisualsContext)
}

export function useVisualsUpdate(){
  return useContext(VisualsUpdateContext)
}

export function DataProvider({ children }) {
  //list of checked datapoints
  const [checkedState, setCheckedState] = useState(
    Object.assign({}, ...allData.map((entry) => ({ [entry.EUNumber]: false })))
  )

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

  //visualisation context to save the visualisations when navigating the page
  const [visuals, setVisuals] = useState([{
    id: 1,
    chart_type: 'bar',
    chartSpecificOptions: {
      xAxis: 'DecisionYear',
      yAxis: 'Rapporteur',
      categoriesSelected: [],
    },
    legend_on: true,
    labels_on: false,
    data: selectedData,
    series: [],
    uniqueCategories: [],
    changeName: '',
  }])

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
