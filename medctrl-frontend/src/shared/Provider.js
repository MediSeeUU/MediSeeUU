import { CheckedProvider } from './Contexts/CheckedContext'
import { ColumnSelectionProvider } from './Contexts/ColumnSelectionContext'
import { DataProvider } from './Contexts/DataContext'
import { SelectedProvider } from './Contexts/SelectedContext'
import { StructureProvider } from './Contexts/StructureContext'
import { TableUtilsProvider } from './Contexts/TableUtilsContext'
import { VisualsProvider } from './Contexts/VisualsContext'

// General provider component that provides all the stored data to the application
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
