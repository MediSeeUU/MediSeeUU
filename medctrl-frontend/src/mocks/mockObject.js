import allServerData from '../json/allServerData.json'
import structServerData from '../json/structServer.json'
import cleanFetchedData from '../shared/Contexts/format'

const obj = {
  data: cleanFetchedData(allServerData, structServerData),
  struct: structServerData,
}

export default obj
