import React from 'react';
import ReactDOM from 'react-dom';
import './css/index.css';
import App from './App';
import VisualizationPage from "./visualizations/visualization_page";

ReactDOM.render(
  <React.StrictMode>
    <VisualizationPage />
  </React.StrictMode>,
  document.getElementById('root')
);
