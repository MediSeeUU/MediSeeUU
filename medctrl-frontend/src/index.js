import React from 'react';
import ReactDOM from 'react-dom';
import './css/index.css';
import Table from './components/table/table';
import DummyData from './json/small_data.json';

ReactDOM.render(
  <React.StrictMode>
    <Table data={DummyData} />
  </React.StrictMode>,
  document.getElementById('root')
);
