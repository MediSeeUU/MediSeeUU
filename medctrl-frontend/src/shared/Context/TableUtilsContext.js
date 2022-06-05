import React, { useContext, useState } from 'react'

const TableUtilsContext = React.createContext()

export function useTableUtils() {
  return useContext(TableUtilsContext)
}

export function TableUtilsProvider({ children }) {
  const [tableUtils, setTableUtils] = useState({
    search: '',
    filters: [
      {
        selected: '',
        input: [{ var: '', filterRange: 'from' }],
        filterType: '',
      },
    ],
    sorters: [{ selected: '', order: 'asc' }],
  })

  return (
    <TableUtilsContext.Provider value={{tableUtils, setTableUtils}}>
      {children}
    </TableUtilsContext.Provider>
  )
}
