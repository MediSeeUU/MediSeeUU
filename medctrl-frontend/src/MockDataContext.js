import { StaticDataProvider } from './shared/Context/DataContext'
import cleanFetchedData from './shared/Context/DataParsing'
import allServerData from './allServerData.json'
import structServerData from './structServer.json'

export default function MockDataProvider({ children }) {
  const cleanedData = cleanFetchedData(allServerData, structServerData)
  return (
    <StaticDataProvider allData={cleanedData} structData={structServerData}>
      {children}
    </StaticDataProvider>
  )
}
