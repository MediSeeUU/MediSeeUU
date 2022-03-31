import React from 'react'
import ReactDOM from 'react-dom'
import App from './core/app/App'
import './index.css'

import Table from './shared_components/table/table';
import Data from './json/data.json';

ReactDOM.render(
  <React.StrictMode>
    <Table data={Data} />
  </React.StrictMode>,
  document.getElementById('root')
)
