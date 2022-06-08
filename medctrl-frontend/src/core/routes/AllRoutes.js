// This program has been developed by students from the bachelor Computer Science at
// Utrecht University within the Software Project course.
// © Copyright Utrecht University (Department of Information and Computing Sciences)
import HomePage from '../../pages/home/HomePage'
import InfoPage from '../../pages/info/InfoPage'
import DataPage from '../../pages/data/DataPage'
import SettingsPage from '../../pages/settings/SettingsPage'
import AccountPage from '../../pages/account/AccountPage'
import VisualizationPage from '../../pages/visualizations/VisualizationPage'
import DetailedInfoPage from '../../pages/detailed-info/DetailedInfoPage'
import ErrorPage from '../../pages/error/ErrorPage'

import { Routes, Route } from 'react-router-dom'

function AllRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/info" element={<InfoPage />} />
      <Route path="/data" element={<DataPage />} />
      <Route path="/visualizations" element={<VisualizationPage />} />
      <Route path="/colors" element={<SettingsPage />} />
      <Route path="/account" element={<AccountPage />} />
      <Route path="/details/:medID" element={<DetailedInfoPage />} />
      <Route path="/*" element={<ErrorPage />} />
    </Routes>
  )
}

export default AllRoutes
