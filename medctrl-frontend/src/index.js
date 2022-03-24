import React from 'react';
import ReactDOM from 'react-dom';
import './css/index.css';
import App from './App';
import Table from './shared_components/table/table'
import DummyData from './json/small_data.json'

ReactDOM.render(
  <React.StrictMode>
    <Table initData={DummyData}
           selectTable={true}/>
  </React.StrictMode>,
  document.getElementById('root')
);
