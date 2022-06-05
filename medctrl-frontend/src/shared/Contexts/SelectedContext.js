import React, { useContext } from 'react'
import { useCheckedState } from './CheckedContext'
import { useData } from './DataContext'

const SelectedContext = React.createContext()

export function useSelectedData() {
  return useContext(SelectedContext)
}

export function SelectedProvider({ children }) {
  const data = useData()
  const { checkedState } = useCheckedState()

  //selected datalist
  const selectedData = data.filter((item, index) => {
    return checkedState[item.EUNoShort]
  })

  return (
    <SelectedContext.Provider value={selectedData}>
      {children}
    </SelectedContext.Provider>
  )
}
