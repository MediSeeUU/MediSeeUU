import React from 'react';
import ReactDOM from 'react-dom';
import './css/index.css';
import App from './App';

import Table from './shared_components/table/table';
import Data from './json/data.json';

ReactDOM.render(
  <React.StrictMode>
    <Table data={Data} />
  </React.StrictMode>,
  document.getElementById('root')
);
