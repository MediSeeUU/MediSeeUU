import './App.css'
import { BrowserRouter } from 'react-router-dom'
import SideNavigation from '../navigation/Navigation'
import AllRoutes from '../routes/AllRoutes.js'
import Header from '../header/Header'
import Footer from '../footer/Footer'
import { DataProvider } from '../../shared/contexts/DataContext'
import DashboardTour from '../tour/DashboardTour'
import React from 'react'

function App() {
  return (
    <BrowserRouter basename={process.env.PUBLIC_URL}>
      <div className="med-page-wrapper">
        <Header />
        <SideNavigation />
        <main className="med-content">
          <div className="med-content-wrapper">
            <DataProvider>
              <DashboardTour>
                <AllRoutes />
              </DashboardTour>
            </DataProvider>
          </div>
          <Footer />
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
