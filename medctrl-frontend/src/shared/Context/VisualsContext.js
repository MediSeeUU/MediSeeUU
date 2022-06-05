import React, { useContext, useState, useEffect } from 'react'
import GetUniqueCategories from '../../pages/visualizations/single_visualization/utils/GetUniqueCategories'
import { useData } from './DataContext'

const VisualsContext = React.createContext()

export function useVisuals() {
  return useContext(VisualsContext)
}

export function VisualsProvider({ children }) {
  const data = useData()

  // visualisation context to save the visualisations when navigating the page
  const [visuals, setVisuals] = useState([])

  // update the visualisation context state when the allData state is changed
  useEffect(() => {
    if (data.length > 0) {
      let uniqueCategories = GetUniqueCategories(data)
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
        },
      ])
    }
  }, [data])

  return (
    <VisualsContext.Provider value={{ visuals, setVisuals }}>
      {children}
    </VisualsContext.Provider>
  )
}
