// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import { CheckedProvider } from './contexts/CheckedContext'
import { ColumnSelectionProvider } from './contexts/ColumnSelectionContext'
import { DataProvider } from './contexts/DataContext'
import { SelectedProvider } from './contexts/SelectedContext'
import { StructureProvider } from './contexts/StructureContext'
import { TableUtilsProvider } from './contexts/TableUtilsContext'
import { VisualsProvider } from './contexts/VisualsContext'

// General provider component that provides all the stored data
// to all the other components of the application
function Provider({ mock, children }) {
  return (
    <StructureProvider mock={mock ? mock.struct : null}>
      <DataProvider mock={mock ? mock.data : null}>
        <CheckedProvider>
          <SelectedProvider>
            <ColumnSelectionProvider>
              <TableUtilsProvider>
                <VisualsProvider>{children}</VisualsProvider>
              </TableUtilsProvider>
            </ColumnSelectionProvider>
          </SelectedProvider>
        </CheckedProvider>
      </DataProvider>
    </StructureProvider>
  )
}

export default Provider
