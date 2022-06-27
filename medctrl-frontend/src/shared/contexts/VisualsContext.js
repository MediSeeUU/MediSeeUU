// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React, { useContext, useState } from 'react'

// Create a new React context for the visualizations data
export const VisualsContext = React.createContext()

// Function that returns the context such that the data can be used in other components
export function useVisuals() {
  return useContext(VisualsContext)
}

// Provider component that provides the visualizations data in the application
export function VisualsProvider({ children }) {
  // Initialize the visualizations state with one visualization
  const [visuals, setVisuals] = useState([
    {
      id: 1,
      chartType: 'bar',
      chartSpecificOptions: {
        xAxis: 'DecisionYear',
        yAxis: 'Rapporteur',
      },
      legendOn: false,
      labelsOn: false,
    },
  ])

  return (
    <VisualsContext.Provider value={{ visuals, setVisuals }}>
      {children}
    </VisualsContext.Provider>
  )
}
