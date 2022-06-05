import React, { useContext, useState } from 'react'

const ColumnSelectionContext = React.createContext()

export function useColumnSelection() {
  return useContext(ColumnSelectionContext)
}

export function ColumnSelectionProvider({ children }) {
  //the column selection state with the default columns on key names
  const [columnSelection, setColumnSelection] = useState([
    'EUNoShort',
    'BrandName',
    'MAH',
    'DecisionDate',
    'ATCCodeL2',
  ])

  return (
    <ColumnSelectionContext.Provider
      value={{ columnSelection, setColumnSelection }}
    >
      {children}
    </ColumnSelectionContext.Provider>
  )
}
