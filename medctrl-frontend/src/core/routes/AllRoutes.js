import HomePage from '../../pages/home/HomePage'
import SearchPage from '../../pages/search/SearchPage'
import DataPage from '../../pages/data/DataPage'
import MessagesPage from '../../pages/messages/MessagesPage'
import SettingsPage from '../../pages/settings/SettingsPage'
import AccountPage from '../../pages/account/AccountPage'
import { Routes, Route } from 'react-router-dom'
import VisualizationPage from '../../pages/visualizations/visualization_page'
import { useSelectedData } from '../../shared/contexts/DataContext'

function AllRoutes() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/search" element={<SearchPage />} />
      <Route path="/data" element={<DataPage />} />
      <Route path="/visualizations" element={<VisualizationPage selectedData={useSelectedData()} />} />
      <Route path="/messages" element={<MessagesPage />} />
      <Route path="/settings" element={<SettingsPage />} />
      <Route path="/account" element={<AccountPage />} />
    </Routes>
  )
}

export default AllRoutes
