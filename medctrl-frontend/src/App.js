import './css/App.css';
import React, { useState } from 'react';
import Table from './shared_components/table/table'
import DummyData from './json/data.json'

function App() {
  const allData = DummyData
  let selectedData = [];

  const dataToApp = (childData) => {
    selectedData = childData;
  }

  return (
    <Table data={allData}/>
  );
}

export default App;