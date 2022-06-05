import React, { useContext, useState, useEffect } from 'react'
import { useData } from './DataContext'

const CheckedContext = React.createContext()

export function useCheckedState() {
  return useContext(CheckedContext)
}

export function CheckedProvider({ children }) {
  const data = useData()

  //list of checked datapoints
  const [checkedState, setCheckedState] = useState(
    Object.assign({}, ...data.map((entry) => ({ [entry.EUNoShort]: true })))
  )

  // update the checked datapoints state when the allData state is changed
  useEffect(() => {
    setCheckedState(
      Object.assign(
        {},
        ...data.map((entry) => ({ [entry.EUNoShort]: true }))
      )
    )
  }, [data])

  return (
    <CheckedContext.Provider value={{checkedState, setCheckedState}}>
      {children}
    </CheckedContext.Provider>
  )
}
