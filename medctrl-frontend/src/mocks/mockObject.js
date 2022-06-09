import allServerData from '../json/allServerData.json'
import structServerData from '../json/structServer.json'
import cleanFetchedData from '../shared/Contexts/format'

// Create an object that contains the mocked medicines and structure data
const mockObj = {
  data: cleanFetchedData(allServerData, structServerData),
  struct: structServerData,
}

export default mockObj
