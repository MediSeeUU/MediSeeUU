import App from '../App.js'
import ReactDOM from 'react-dom'

test('App component renders without crashing', () => {
  const root = document.createElement('div')
  ReactDOM.render(App(), root)
})
