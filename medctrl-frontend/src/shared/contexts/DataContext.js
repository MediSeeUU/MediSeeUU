import React, { useContext, useState } from 'react'
import allData from '../../testJson/data.json'

export const DataContext = React.createContext()
export const SelectedContext = React.createContext()
export const CheckedContext = React.createContext()
export const CheckedContextUpdate = React.createContext()
export const ColumnSelectionContext = React.createContext()
export const ColumnSelectionContextUpdate = React.createContext()

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

  return (
    <DataContext.Provider value={allData}>
      <SelectedContext.Provider value={selectedData}>
        <CheckedContext.Provider value={checkedState}>
          <CheckedContextUpdate.Provider value={setCheckedState}>
            <ColumnSelectionContext.Provider value={columnSelection}>
              <ColumnSelectionContextUpdate.Provider value={setColumnSelection}>
                {children}
              </ColumnSelectionContextUpdate.Provider>
            </ColumnSelectionContext.Provider>
          </CheckedContextUpdate.Provider>
        </CheckedContext.Provider>
      </SelectedContext.Provider>
    </DataContext.Provider>
  )
}
