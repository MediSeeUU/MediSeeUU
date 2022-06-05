import { CheckedProvider } from './Contexts/CheckedContext'
import { ColumnSelectionProvider } from './Contexts/ColumnSelectionContext'
import { DataProvider } from './Contexts/DataContext'
import { SelectedProvider } from './Contexts/SelectedContext'
import { StructureProvider } from './Contexts/StructureContext'
import { TableUtilsProvider } from './Contexts/TableUtilsContext'
import { VisualsProvider } from './Contexts/VisualsContext'

function Provider({ children }) {
  return (
    <StructureProvider>
      <DataProvider>
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
