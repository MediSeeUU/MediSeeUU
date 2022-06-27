// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

// react-testing-library renders your components to document.body,
// this adds jest-dom's custom assertions

import '@testing-library/jest-dom'
import './mocks/mockApi'

console.error = (err) => {
  throw new Error(err)
}

console.warn = (warning) => {
  throw new Error(warning)
}
