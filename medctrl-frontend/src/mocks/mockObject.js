// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import allServerData from '../json/allServerData.json'
import structServerData from '../json/structServer.json'
import cleanFetchedData from '../shared/contexts/format'

// Create an object that contains the mocked medicines and structure data
const mockObj = {
  data: cleanFetchedData(allServerData, structServerData),
  struct: structServerData,
}

export default mockObj
