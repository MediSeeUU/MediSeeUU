// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import Provider from '../shared/Provider'
import mockObject from './mockObject'

// Function based component that mocks the provider
// This is used to be able to unit test components that need certain data
function MockProvider({ mock, children }) {
  return <Provider mock={mock || mockObject}>{children}</Provider>
}

export default MockProvider
