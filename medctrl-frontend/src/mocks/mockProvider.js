import Provider from '../shared/Provider'
import mockObject from './mockObject'

function MockProvider({ mock, children }) {
  return <Provider mock={mock || mockObject}>{children}</Provider>
}

export default MockProvider
