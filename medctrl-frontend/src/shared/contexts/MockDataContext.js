// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import { StaticDataProvider } from './DataContext'
import cleanFetchedData from './DataParsing'
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
