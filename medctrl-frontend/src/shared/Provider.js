import { CheckedProvider } from "./Context/CheckedContext"
import { ColumnSelectionProvider } from "./Context/ColumnSelectionContext"
import { DataProvider } from "./Context/DataContext"
import { SelectedProvider } from "./Context/SelectedContext"
import { StructureProvider } from "./Context/StructureContext"
import { TableUtilsProvider } from "./Context/TableUtilsContext"
import { VisualsProvider } from "./Context/VisualsContext"

function Provider({ children }) {
  return (
    <StructureProvider>
      <DataProvider>
        <CheckedProvider>
          <SelectedProvider>
            <ColumnSelectionProvider>
              <TableUtilsProvider>
                <VisualsProvider>
                  {children}
                </VisualsProvider>
              </TableUtilsProvider>
            </ColumnSelectionProvider>
          </SelectedProvider>
        </CheckedProvider>
      </DataProvider>
    </StructureProvider>
  )
}

export default Provider
