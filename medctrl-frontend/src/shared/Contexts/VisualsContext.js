import React, { useContext, useState, useEffect } from 'react'
import GetUniqueCategories from '../../pages/visualizations/single_visualization/utils/GetUniqueCategories'
import { useData } from './DataContext'

// Create a new React context for the visualizations data
const VisualsContext = React.createContext()

// Function that returns the context such that the data can be used in other components
export function useVisuals() {
  return useContext(VisualsContext)
}

// Provider component that provides the visualizations data in the application
export function VisualsProvider({ mock, children }) {
  // The medicines data is necessary to determine the selected categories
  const data = useData()

  // Initialize the visualizations state with one visualization
  const [visuals, setVisuals] = useState([
    {
      id: 1,
      chartType: 'bar',
      chartSpecificOptions: {
        xAxis: 'DecisionYear',
        yAxis: 'Rapporteur',
        categoriesSelectedY: [],
        categoriesSelectedX: [],
      },
      legendOn: false,
      labelsOn: false,
    },
  ])

  // Update the selected categories if the medicines data is retrieved
  useEffect(() => {
    if (!mock && data.length > 0) {
      let uniqueCategories = GetUniqueCategories(data)
      visuals[0].chartSpecificOptions.categoriesSelectedY = uniqueCategories['Rapporteur']
      visuals[0].chartSpecificOptions.categoriesSelectedX = uniqueCategories['DecisionYear']
      setVisuals(visuals)
    }
  }, [data, mock, visuals])

  return (
    <VisualsContext.Provider value={{ visuals, setVisuals }}>
      {children}
    </VisualsContext.Provider>
  )
}
