import Provider from '../shared/Provider'
import mockObject from './mockObject'

// Function based component that mocks the provider
// This is used to be able to unit test components that need certain data
function MockProvider({ mock, children }) {
  return <Provider mock={mock || mockObject}>{children}</Provider>
}

export default MockProvider
