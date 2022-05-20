import { StaticDataProvider } from './DataContext'
import cleanFetchedData from './DataParsing'
import allServerData from './allServerData.json'

export default function MockDataProvider({ children }) {
  const cleanedData = cleanFetchedData(allServerData)
  return (
    <StaticDataProvider allData={cleanedData}>{children}</StaticDataProvider>
  )
}
