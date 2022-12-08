// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)

import React from 'react'
import { Routes, Route } from 'react-router-dom'
import HomePage from '../pages/home/HomePage'
import InfoPage from '../pages/info/InfoPage'
import DataPage from '../pages/data/DataPage'
import OrphanPage from '../pages/orphan/OrphanPage'
import AccountPage from '../pages/account/AccountPage'
import VisualizationPage from '../pages/visualizations/VisualizationPage'
import DetailedInfoPage from '../pages/detailed-info/DetailedInfoPage'
import ErrorPage from '../pages/error/ErrorPage'

// Returns the routing information to be able to navigate to different pages
function Routing() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/info" element={<InfoPage />} />
      <Route path="/data" element={<DataPage />} />
      <Route path="/orphan" element={<OrphanPage />} />
      <Route path="/visualizations" element={<VisualizationPage />} />
      <Route path="/account" element={<AccountPage />} />
      <Route path="/details/:medID" element={<DetailedInfoPage />} />
      <Route path="/*" element={<ErrorPage />} />
    </Routes>
  )
}

export default Routing
