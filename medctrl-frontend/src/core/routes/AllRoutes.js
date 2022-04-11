import HomePage from '../../pages/home/HomePage'
import SearchPage from '../../pages/search/SearchPage'
import DataPage from '../../pages/data/DataPage'
import MessagesPage from '../../pages/messages/MessagesPage'
import SettingsPage from '../../pages/settings/SettingsPage'
import AccountPage from '../../pages/account/AccountPage'
import VisualizationPage from '../../pages/visualizations/visualization_page'
import DetailedInfoPage from '../../pages/detailed-info/DetailedInfoPage'

import { Routes, Route } from 'react-router-dom'

function AllRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/search" element={<SearchPage />} />
      <Route path="/data" element={<DataPage />} />
      <Route path="/visualizations" element={<VisualizationPage />} />
      <Route path="/messages" element={<MessagesPage />} />
      <Route path="/settings" element={<SettingsPage />} />
      <Route path="/account" element={<AccountPage />} />
      <Route path="/details" element={<DetailedInfoPage />} />
    </Routes>
  )
}

export default AllRoutes
