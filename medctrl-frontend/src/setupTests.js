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
