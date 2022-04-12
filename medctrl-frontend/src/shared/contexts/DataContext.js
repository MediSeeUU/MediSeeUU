import React, { useContext, useState } from 'react'
import allData from '../../testJson/data.json'

export const DataContext = React.createContext()
export const SelectedContext = React.createContext()
export const CheckedContext = React.createContext()
export const CheckedContextUpdate = React.createContext()

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

export function DataProvider({ children }) {
  const [checkedState, setCheckedState] = useState(
    Object.assign({}, ...allData.map((entry) => ({ [entry.EUNumber]: false })))
  )
  const selectedData = allData.filter((item, index) => {
    return checkedState[item.EUNumber]
  })

  return (
    <DataContext.Provider value={allData}>
      <SelectedContext.Provider value={selectedData}>
        <CheckedContext.Provider value={checkedState}>
          <CheckedContextUpdate.Provider value={setCheckedState}>
            {children}
          </CheckedContextUpdate.Provider>
        </CheckedContext.Provider>
      </SelectedContext.Provider>
    </DataContext.Provider>
  )
}
